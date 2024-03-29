from datetime import date
from fastapi import APIRouter, Depends
from pydantic.v1 import parse_obj_as
from sqlalchemy import select

from app.bookings.models import Bookings
from app.bookings.dao import BookingDAO
from app.bookings.schamas import SBooking
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("")
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict


@router.delete("")
async def remove_booking(booking_id: int, current_user: Users = Depends(get_current_user)):
    await BookingDAO.delete_booking(booking_id, current_user)