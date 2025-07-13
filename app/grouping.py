from sqlalchemy.orm import Session
from sqlalchemy.sql import text

def group_trips(db: Session):
    query = text("""
        SELECT
            region,
            time_of_day,
            ST_AsText(origin) AS origin_point,
            ST_AsText(destination) AS destination_point,
            COUNT(*) as total_trips
        FROM trips
        GROUP BY region, time_of_day, origin_point, destination_point
        ORDER BY total_trips DESC;
    """)
    result = db.execute(query)
    return result.mappings().all()  # <-- alteração aqui

