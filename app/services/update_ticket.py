import requests
import time
from flask import current_app

from app.utils.validation_models import UpdateReservation, UpdatePassengers
from app.utils.custom_exception import MIMETYPE_NOT_SUPPORTED
from app.services.fetch_ticket_details import fetch_ticket

def update_ticket(reservationId, request):
    if request.is_json:
        request_body = request.json
    else:
        raise MIMETYPE_NOT_SUPPORTED(f"Request Body's Media Type is not supported. Ticket booking system accepts only application/json MIME Type")
    
    passengers = list(map(lambda passenger: UpdatePassengers(
        passengerId=passenger.get("passengerId"),
        coachNumber=passenger.get("coachNumber"),
        seatNumber=passenger.get("seatNumber")
    ), request_body.get("passengerPreferences")))

    reservation = UpdateReservation(
        status=request_body.get("status"),
        passengerPreferences=passengers
    )
    
    ticketDetails = fetch_ticket(reservationId)

    ticketDetails["status"] = reservation.status
    ticketDetails["passengers"] = passengers

    '''req_body = {
        "status": payload.status,
        "passengers": payload.passengerPreferences map do{
            var passenger = (ticketDetails.passengers filter((item, ind) -> (item.passengerId == $.passengerId)))[0]
            ---
            {
                "passengerId": $.passengerId,
                "coachNumber": $.coachNumber,
                "seatNumber": $.seatNumber,
                "name": $.name default passenger.name,
                "age": $.age default passenger.age,
                "gender": $.gender default passenger.gender,
                "classType": passenger.classType
            }	
	    }
    }'''

    #update request call
    
    return {
        "message": "Reservation details updated successfully",
        "reservationId": reservationId,
        "travelDate": ticketDetails.get("travelDate"),
        "trainId": ticketDetails.get("trainId"),
        "dateTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    }