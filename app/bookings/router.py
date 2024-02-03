from fastapi import APIRouter
from sqlalchemy import select

from app.bookings.models import Bookings
from app.bookings.dao import BookingDAO


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings():
    return await BookingDAO.find_one_or_none(room_id=2)

        