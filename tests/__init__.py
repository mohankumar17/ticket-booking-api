import pandas as pd

class UpdatePassengers:
    def __init__(self, passengerId:str, coachNumber:str, seatNumber:int) -> None:
        self.passengerId = passengerId
        self.coachNumber = coachNumber
        self.seatNumber = seatNumber

def updatedPassengers():
    passengers = pd.DataFrame([
        {'passengerId': 'P3', 'name': 'John Doe', 'age': 30, 'gender': 'Male', 'classType': 'General', 'coachNumber': None, 'seatNumber': None}, 
        {'passengerId': 'P4', 'name': 'Paul Brandon', 'age': 34, 'gender': 'Male', 'classType': '2AC', 'coachNumber': None, 'seatNumber': None},
        {'passengerId': 'P5', 'name': 'Alex Turing', 'age': 27, 'gender': 'Male', 'classType': '3AC', 'coachNumber': "SL12", 'seatNumber': "56"}
    ])
    passengers = passengers.drop(["coachNumber", "seatNumber"], axis=1) #axis=1 indicates columns

    ticketDetails = [
        UpdatePassengers(passengerId='P3', coachNumber='C12', seatNumber=22), 
        UpdatePassengers(passengerId='P4', coachNumber='A5', seatNumber=7)
    ]

    ticketDetails = pd.DataFrame(list(map(lambda ticket: ticket.__dict__,ticketDetails)))
    passengers = pd.merge(left=passengers, right=ticketDetails, on="passengerId", how="inner")

    print(passengers.to_dict(orient="records"))


if __name__ == "__main__":
    updatedPassengers()



