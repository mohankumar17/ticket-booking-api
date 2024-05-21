from flask import Flask
import logging
from app.configurations import Config

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    app.logger.setLevel(logging.DEBUG)

    from app.routes.ticket_booking import ticket_booking_bp
    app.register_blueprint(ticket_booking_bp)

    return app