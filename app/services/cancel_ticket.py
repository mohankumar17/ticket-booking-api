from flask import current_app
import requests
import time

def cancel_ticket(reservationId):
    url = f'http://{current_app.config.get("RESERVATIONS_API_HOST")}:{current_app.config.get("RESERVATIONS_API_PORT")}/api/reservations/{reservationId}'
    res = requests.delete(url=url)

    if res.status_code == 200:
        return {
            "message": "Reservation cancelled successfully",
            "reservationId": reservationId,
            "dateTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
        }
    else:
        raise Exception("Reservation details not found")