from fastapi import FastAPI, Query, Depends

from typing import Optional
from datetime import date
from pydantic import BaseModel

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.pages.router import router as router_pages


app = FastAPI()


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)


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

# if __name__ == '__main__':
#     print_hi('PyCharm')


