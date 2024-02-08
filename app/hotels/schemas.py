from datetime import date
from pydantic import BaseModel


class Hotel(BaseModel):
    id: int
    name: str
    location: str
    services: str
    room_quantity: int
    image_id: int


class HotelInfo(BaseModel):
    pass


class RoomInfo(BaseModel):
    pass