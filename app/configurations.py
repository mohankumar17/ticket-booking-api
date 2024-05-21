import yaml

class Config:
    with open("config/dev.yaml") as config_file:
        properties = yaml.safe_load(config_file)
    
    HTTP_HOST = properties["http"]["host"]
    HTTP_PORT = properties["http"]["port"]

    RESERVATIONS_API_HOST = properties["railway_reservation_api"]["host"]
    RESERVATIONS_API_PORT = properties["railway_reservation_api"]["port"]

    TRAINS_API_HOST = properties["train_details_api"]["host"]
    TRAINS_API_PORT = properties["train_details_api"]["port"]

    PASSENGERS_API_HOST = properties["passengers_poi_api"]["host"]
    PASSENGERS_API_PORT = properties["passengers_poi_api"]["port"]
    PASSENGERS_API_BUCKET = properties["passengers_poi_api"]["storageBucket"]
