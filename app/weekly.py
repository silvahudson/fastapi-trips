from sqlalchemy.orm import Session
from sqlalchemy import text

def weekly_average_by_region(db: Session, region: str):
    query = text("""
        SELECT date_trunc('week', datetime) AS week,
               COUNT(*) AS trips
        FROM trips
        WHERE region = :region
        GROUP BY week
        ORDER BY week;
    """)
    result = db.execute(query, {"region": region}).mappings().all()
    return result

