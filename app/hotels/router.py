import asyncio
from datetime import date, datetime
from fastapi_cache.decorator import cache
from typing import List
from fastapi import APIRouter, Query
from pydantic.v1 import parse_obj_as

from app.hotels.dao import HotelDAO
from app.hotels.schemas import HotelInfo, RoomInfo


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{location}")
@cache(expire=20)
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {datetime.now().date()}"),):
    # await asyncio.sleep(3)
    hotels = await HotelDAO.search_for_hetels(location, date_from, date_to)
    hotels_json = parse_obj_as(List[HotelInfo], hotels)
    return hotels_json


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_time(
    hotel_id: int,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {datetime.now().date()}"),) -> List[RoomInfo]:
    rooms = await HotelDAO.search_for_hetels(hotel_id, date_from, date_to)
    return rooms