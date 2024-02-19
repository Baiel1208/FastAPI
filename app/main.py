from fastapi import FastAPI, Query, Depends
from fastapi.staticfiles import StaticFiles

from typing import Optional
from datetime import date
from pydantic import BaseModel
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin

from app.bookings.router import router as router_bookings
from app.config import settings
from app.users.models import Users
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.pages.router import router as router_pages
from app.images.router import router as router_images

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
from sqladmin import Admin, ModelView

from app.database import engine
from app.admin.auth import authentication_backend


app = FastAPI()

app.mount("/static", StaticFiles(directory='app/static'), 'static')


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)


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


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://{settings.REIDS_HOST}:{settings.REIDS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)