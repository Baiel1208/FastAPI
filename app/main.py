from fastapi import FastAPI, Query, Depends

from typing import Optional
from datetime import date
from pydantic import BaseModel


app = FastAPI()


class SHotelSearchArgs:
    def __init__(
            self,
        location: str,
        date_from: date,
        date_to: date,
        has_spa: Optional[bool] = Query(None, ge=1, le=5),
        stars: Optional[int] = None
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars


@app.get('/hotels')
def get_hotels(search_args: SHotelSearchArgs=Depends()):
    return search_args


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/bookings")
def add_booking(booking: SBooking):
    pass
# if __name__ == '__main__':
#     print_hi('PyCharm')

