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
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: str
    quantity: int
    image_id: int