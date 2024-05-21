import requests
import pandas as pd
import time
from flask import current_app

from app.utils.validation_models import UpdateReservation, UpdatePassengers
from app.utils.custom_exception import MIMETYPE_NOT_SUPPORTED
from app.services.fetch_ticket import fetch_ticket

def update_ticket(reservationId, request):
    if request.is_json:
        request_body = request.json
    else:
        raise MIMETYPE_NOT_SUPPORTED(f"Request Body's Media Type is not supported. Ticket booking system accepts only application/json MIME Type")
    
    passengerPositions = list(map(lambda passenger: UpdatePassengers(
        passengerId=passenger.get("passengerId"),
        coachNumber=passenger.get("coachNumber"),
        seatNumber=passenger.get("seatNumber")
    ), request_body.get("passengerPreferences")))

    reservation = UpdateReservation(
        status=request_body.get("status"),
        passengerPreferences=passengerPositions
    )

    passengerPositions = pd.DataFrame(list(map(lambda pos: pos.__dict__, passengerPositions))) #left

    ticketDetails = fetch_ticket(reservationId)

    passengerDetails = pd.DataFrame(ticketDetails.get("passengers")) #right
    passengerDetails = passengerDetails.drop(["coachNumber", "seatNumber"], axis=1) #axis=1 indicates columns

    updatedPassengers = pd.merge(left=passengerPositions, right=passengerDetails, on="passengerId", how="inner")
    updatedPassengers = updatedPassengers.to_dict(orient="records")

    ticketDetails["status"] = reservation.status
    ticketDetails["passengers"] = updatedPassengers

    current_app.logger.info(ticketDetails)

    #update request call
    url = f'http://{current_app.config.get("RESERVATIONS_API_HOST")}:{current_app.config.get("RESERVATIONS_API_PORT")}/api/reservations/{reservationId}'
    res = requests.put(url=url, json=ticketDetails)

    if res.status_code != 200:
        raise Exception("Unable to update reservation details!!")
    
    return {
        "message": "Reservation details updated successfully",
        "reservationId": reservationId,
        "travelDate": ticketDetails.get("travelDate"),
        "trainId": ticketDetails.get("trainId"),
        "dateTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    }