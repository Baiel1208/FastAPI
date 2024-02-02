from fastapi import FastAPI, Query

from typing import Optional
from datetime import date
from pydantic import BaseModel


app = FastAPI()


class SHotel(BaseModel):
    address: str
    name: str
    stars: int



@app.get('/hotels')
def get_hotels(location: str,
               date_from: date,
               date_to: date,
               has_spa: Optional[bool] = Query(None, ge=1, le=5),
               stars: Optional[int] = None) -> list[SHotel]:
    hotels = [
        {
            'address': 'ул. Ленин, 1, Ош',
            'name': 'Super Hotel',
            'stars': 5
        }
    ]
    return hotels

class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date
@app.post("/bookings")
def add_booking(booking: SBooking):
    pass
# if __name__ == '__main__':
#     print_hi('PyCharm')


