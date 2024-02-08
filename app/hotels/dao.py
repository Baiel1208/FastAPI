from app.dao.base import BaseDAO
from app.hotels.models import Hotels, Rooms


class HotelDAO(BaseDAO):
    model = Hotels


    @classmethod
    async def find_all():
        pass


class RoomDAO(BaseDAO):
    model = Rooms