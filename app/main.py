from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy.orm import Session
import asyncio
from threading import Thread
import time

from .db import SessionLocal, engine
from .models import Base
from .ingestion import ingest_csv
from .grouping import group_trips
from .weekly import weekly_average_by_region

app = FastAPI(title="Trip Ingestion API")

Base.metadata.create_all(bind=engine)

ingestion_status = {"status": "idle"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/ingest")
def ingest_data(db: Session = Depends(get_db)):
    ingest_csv(db)
    return {"message": "Ingestion completed successfully"}

@app.post("/ingest_async")
def ingest_data_ws(db: Session = Depends(get_db)):
    def run_ingest():
        ingestion_status["status"] = "running"
        ingest_csv(db)
        ingestion_status["status"] = "completed"
        time.sleep(5)
        ingestion_status["status"] = "idle"
    Thread(target=run_ingest).start()
    return {"message": "Ingestion started"}

@app.websocket("/ws/ingestion")
async def websocket_ingestion_status(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json(ingestion_status)
        await asyncio.sleep(1)

@app.get("/grouped")
def get_grouped_trips(db: Session = Depends(get_db)):
    grouped = group_trips(db)
    return {"groups": grouped}

@app.get("/weekly_avg")
def get_weekly_avg(region: str, db: Session = Depends(get_db)):
    data = weekly_average_by_region(db, region)
    return {"region": region, "weekly_average": data}
