from flask import current_app
import time
import requests
from app.utils.custom_exception import MIMETYPE_NOT_SUPPORTED
from app.utils.validation_models import Reservation, Passenger, Proof
from app.services.fetch_train_details import train_details

def get_fare_price(train_data, ticket):
    total_fare = 0
    haltStation = list(filter(lambda station: station.get("stationId") == ticket.sourceStation,
        train_data.get("haltStations")
    ))[0]
    priceDetails = list(filter(lambda station: station.get("stationId") == ticket.destinationStation,
        haltStation.get("nextStations")
    ))[0]

    for passenger in ticket.passengerPreferences:
        total_fare += priceDetails.get("prices").get(passenger.classType)

    return total_fare

def create_new_reservation(req_body):
    url = f'http://{current_app.config.get("RESERVATIONS_API_HOST")}:{current_app.config.get("RESERVATIONS_API_PORT")}/api/reservations'
    res = requests.post(url=url, json=req_body)

    if res.status_code == 201:
        return res.json().get("reservationId")
    else:
        raise Exception("Unable to make new reservation entry!!")
    
def upload_identity_doc(req_body):
    url = f'http://{current_app.config.get("PASSENGERS_API_HOST")}:{current_app.config.get("PASSENGERS_API_PORT")}/api/upload'
    res = requests.post(url=url, json=req_body)

    if res.status_code != 200:
        raise Exception("Passenger Identity Proof Upload Failed!!")

def book_ticket(request):
    if request.is_json:
        request_body = request.json
    else:
        raise MIMETYPE_NOT_SUPPORTED(f"Request Body's Media Type is not supported. Ticket booking system accepts only application/json MIME Type")
    
    passengersList = list(map(lambda passenger: Passenger(
            name=passenger.get("name"),
            age=passenger.get("age"),
            gender=passenger.get("gender"),
            classType=passenger.get("classType"),
            proof=Proof(idType=passenger.get("proof").get("idType"), idDocument=passenger.get("proof").get("idDocument"))
        ),
    request_body.get("passengerPreferences")))
    
    ticket = Reservation(
        travelDate=request_body.get("travelDate"),
        trainId=request_body.get("trainId"),
        sourceStation=request_body.get("sourceStation"),
        destinationStation=request_body.get("destinationStation"),
        paymentMethod=request_body.get("paymentMethod"),
        passengerPreferences=passengersList
    )

    train_data = train_details(ticket.trainId)
    total_fare = get_fare_price(train_data, ticket)

    reservation_req = {
        "travelDate": ticket.travelDate,
        "sourceStation": ticket.sourceStation,
	    "destinationStation": ticket.destinationStation,
	    "paymentMethod": ticket.paymentMethod,
	    "totalFare": total_fare,
	    "trainId": ticket.trainId,
	    "passengers": list(map(
            lambda passenger: {
                "passengerId": passenger.passengerId,
                "name": passenger.name,
                "age": passenger.age,
                "gender": passenger.gender,
                "classType": passenger.classType
            },
            ticket.passengerPreferences
        ))
    }

    reservation_id = create_new_reservation(reservation_req)
    
    for passenger in passengersList:
        passenger_id_upload_req = {
            "bucketName": current_app.config.get("PASSENGERS_API_BUCKET"),
            "fileName": str(reservation_id) + "_"  + passenger.passengerId + ".png",
            "document": passenger.proof.idDocument
        }

        upload_identity_doc(passenger_id_upload_req)

    return {
        "message": "Reservation details uploaded successfully",
        "reservationId": reservation_id,
        "travelDate": ticket.travelDate,
        "trainId": ticket.trainId,
        "dateTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    }


