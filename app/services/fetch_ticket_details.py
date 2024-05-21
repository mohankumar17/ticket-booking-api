from flask import current_app
import requests
from app.services.fetch_train_details import train_details

def fetch_ticket(reservationId):
    url = f'http://{current_app.config.get("RESERVATIONS_API_HOST")}:{current_app.config.get("RESERVATIONS_API_PORT")}/api/reservations/{reservationId}'
    res = requests.get(url=url)

    if res.status_code == 200:
        reservation = res.json()
    else:
        raise Exception("Failed to fetch reservation details!!")
    
    train = train_details(reservation.get("trainId"))

    response = {
        "travelDate": reservation.get("travelDate"),
        "trainId": reservation.get("trainId"),
        "trainName": train.get("trainName"),
        "sourceStation": reservation.get("sourceStation"),
        "destinationStation": reservation.get("destinationStation"),
        "paymentMethod": reservation.get("paymentMethod"),
        "totalFare": reservation.get("totalFare"),
        "status": reservation.get("status"),
        "passengers": list(map(lambda passenger : {
            "passengerId": passenger.get("passengerId"),
            "name": passenger.get("name"),
            "age": passenger.get("age"),
            "gender": passenger.get("gender"),
            "classType": passenger.get("classType"),
            "coachNumber": passenger.get("coachNumber"),
            "seatNumber": passenger.get("seatNumber")
        },reservation.get("passengers")))
    }

    return response
