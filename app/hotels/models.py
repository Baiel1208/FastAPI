from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    room_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    room = relationship('Rooms', back_populates='hotel')


    def __str__(self) -> str:
        return f'Отель {self.name} {self.location[:30]}'


class Rooms(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, nullable=False)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=False)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    hotel = relationship('Hotels', back_populates='room')
    booking = relationship('Bookings', back_populates='room')

    def __str__(self) -> str:
        return f'Номер {self.name}'