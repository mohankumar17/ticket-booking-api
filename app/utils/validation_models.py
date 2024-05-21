from pydantic import BaseModel, Field, ValidationError
from typing import Literal, List
from typing import ClassVar
from itertools import count

class Proof(BaseModel):
    idType: str = Field(..., max_length=30)
    idDocument: str = Field(...)

class Passenger(BaseModel):
    _ids: ClassVar[count] = count(1)

    passengerId: str = Field(default_factory=(lambda: "P" + str(next(Passenger._ids))))
    name: str = Field(..., min_length=1, max_length=20)
    age: int = Field(..., ge=0)
    gender: Literal["Male","Female","Others"] = Field(...)
    proof: Proof = Field(...)
    classType: str = Field(..., min_length=1, max_length=30)

class Reservation(BaseModel):

    travelDate: str = Field(...)
    trainId: str = Field(..., min_length=1, max_length=10)
    sourceStation: str = Field(..., min_length=1, max_length=30)
    destinationStation: str = Field(..., min_length=1, max_length=30)
    paymentMethod: str = Field(..., min_length=1, max_length=20)
    passengerPreferences: List[Passenger] = Field(...)

class UpdatePassengers(BaseModel):
    passengerId: str
    coachNumber: str
    seatNumber: int

class UpdateReservation(BaseModel):
    status: Literal["Confirmed", "NotConfirmed"] = Field(...)
    passengerPreferences: List[UpdatePassengers] = Field(...)
