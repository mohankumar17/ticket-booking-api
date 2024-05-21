from flask import Blueprint, current_app, request
import time
import uuid
from pydantic import ValidationError

from app.utils.custom_exception import DETAILS_NOT_FOUND, MIMETYPE_NOT_SUPPORTED
from app.services.book_ticket import book_ticket
from app.services.fetch_ticket import fetch_ticket
from app.services.cancel_ticket import cancel_ticket
from app.services.update_ticket import update_ticket

ticket_booking_bp = Blueprint('ticket_booking', __name__)

# Routers
@ticket_booking_bp.post("/api/bookings/")
def book_ticket_route():
    current_app.logger.info("Book Ticket Route")
    return book_ticket(request)

@ticket_booking_bp.put("/api/bookings/<reservationId>")
def update_ticket_route(reservationId):
    current_app.logger.info("Update Ticket Details Route")
    return update_ticket(reservationId, request)

@ticket_booking_bp.get("/api/bookings/<reservationId>")
def fetch_ticket_route(reservationId):
    current_app.logger.info("Fetch Ticket Details Route")
    return fetch_ticket(reservationId)

@ticket_booking_bp.delete("/api/bookings/<reservationId>")
def cancel_ticket_route(reservationId):
    current_app.logger.info("Cancel Ticket Route")
    return cancel_ticket(reservationId)

############################################################################
'''
Error Handling
    - Global Error Handler: 500
    - Bad Request: 400
    - Not Found: 404
    - Mimetye Not Supported: 415
'''
# Error Handling 
def error_response(errorDetails):
    error_response =  {
        "message": errorDetails.get("message"),
        "description": errorDetails.get("description"),
        "dateTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime()),
        "transactionId": str(uuid.uuid4())
    }
    current_app.logger.error(error_response)
    return error_response

@ticket_booking_bp.errorhandler(ValidationError)
def validation_error_handler(error):
    errorDetails = {
        "message": "Input data validation failed",
        "description": str(error)
    }
    status_code = 400
    response = error_response(errorDetails)
    return response, status_code

@ticket_booking_bp.errorhandler(DETAILS_NOT_FOUND)
def not_found_error_handler(error):
    errorDetails = {
        "message": "Details not found",
        "description": str(error)
    }
    status_code = 404
    response = error_response(errorDetails)
    return response, status_code

@ticket_booking_bp.errorhandler(MIMETYPE_NOT_SUPPORTED)
def mediatype_error_handler(error):
    errorDetails = {
        "message": "Unsupported Media Type",
        "description": str(error)
    }
    status_code = 415
    response = error_response(errorDetails)
    return response, status_code

@ticket_booking_bp.errorhandler(Exception)
def global_error_handler(error):
    errorDetails = {
        "message": "Ticket booking server error",
        "description": str(error)
    }
    status_code = 500
    response = error_response(errorDetails)
    return response, status_code
