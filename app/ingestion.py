import pandas as pd
from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from shapely import wkt
from datetime import datetime

from .models import Trip

def get_time_of_day(hour: int) -> str:
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    elif 18 <= hour < 22:
        return "evening"
    else:
        return "night"

def ingest_csv(db: Session, csv_path: str = "data/trips.csv"):
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        origin = from_shape(wkt.loads(row["origin_coord"]), srid=4326)
        dest = from_shape(wkt.loads(row["destination_coord"]), srid=4326)
        dt = datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M:%S")
        time_of_day = get_time_of_day(dt.hour)

        trip = Trip(
            region=row["region"],
            origin=origin,
            destination=dest,
            datetime=dt,
            datasource=row["datasource"],
            time_of_day=time_of_day
        )
        db.add(trip)

    db.commit()
