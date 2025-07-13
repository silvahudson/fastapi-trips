from sqlalchemy import Column, Integer, String, DateTime
from geoalchemy2 import Geometry
from .db import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, nullable=False)
    origin = Column(Geometry("POINT", srid=4326))
    destination = Column(Geometry("POINT", srid=4326))
    datetime = Column(DateTime)
    datasource = Column(String)
    time_of_day = Column(String)
