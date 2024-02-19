from datetime import date
from sqlalchemy import select, delete, insert, func, and_, or_
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Rooms
from app.database import engine

class BookingDAO(BaseDAO):
    model = Bookings
    

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 4 AND
            (date_from >= '2023-06-01' AND date_from <= '2023-12-18') OR
            (date_to <= '2023-06-01' AND date_to > '2023-06-01')
        )
        """
        async with async_session_maker() as session:
        #     booked_rooms = select(Bookings).where(
        #         and_(
        #             Bookings.room_id == 1,
        #             or_(
        #                 and_(
        #                     Bookings.date_from >= date_from,
        #                     Bookings.date_from <= date_to
        #                 ),
        #                 and_(
        #                     Bookings.date_from <= date_from,
        #                     Bookings.date_to > date_from
        #                 )
        #             )
        #         )
        #     ).cte("booked_rooms")


            """
            select rooms.quantity - count(booked_rooms.room_id) from rooms 
            left join booked_rooms on booked_rooms.room_id = room_id
            where rooms.id = 4
            group by room.quantity, booked_rooms.room_id
            """
            get_rooms_left = select(
                Rooms.quantity - func.count(Bookings.room_id).label("rooms_left")
                ).select_from(Bookings).join(
                    Rooms, Rooms.id == Bookings.room_id, full=True
                ).where(
                    and_(
                        Rooms.id == room_id,
                        or_(
                            Bookings.room_id.is_(None),
                            and_(
                                Bookings.date_from < date_from,
                                Bookings.date_to > date_from
                            ),
                            and_(
                                Bookings.date_from < date_from,
                                Bookings.date_from > date_from
                            )
                        )
                    )
                ).group_by(Rooms.id, Rooms.quantity)

            rooms_left = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()

            # print(get_rooms_left.compile(engine, compile_kwargs={'literal_binds': True}))

            if  not rooms_left or rooms_left > 0:
                get_price = await session.execute(select(Rooms.price).filter_by(id=room_id))
                price = await session.execute(get_price)
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=get_price.scalar(),
                ).returning(Bookings)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()