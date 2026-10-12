"""
api.py
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from db import init_db, get_session, Route
from router import find_routes
from statistics import (
    get_trips_by_route,
    route_stats,
    points_stats,
    popular_routes,
    prediction_diff,
)
from ai_module import analyze, recommend


app = FastAPI(title="AI Navigator")


@app.on_event("startup")
def startup():
    init_db()


# ============================================================
# СХЕМЫ (Pydantic)
# ============================================================

class TripIn(BaseModel):
    start_point: str
    finish_point: str
    route: str
    time: int
    distance: int
    actual_time: int
    actual_distance: int
    traffic: int
    difficulty: int


# ============================================================
# ЭНДПОИНТЫ
# ============================================================

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/routes")
def routes(start: str, finish: str):
    """Возможные маршруты по карте + статистика из БД."""
    paths = find_routes(start, finish)
    if not paths:
        raise HTTPException(status_code=404, detail="Путей не найдено")

    result = []
    session = get_session()
    try:
        for p in paths:
            route_str = ",".join(p["route"])
            stats = route_stats(session, route_str)
            result.append({
                "route": route_str,
                "route_list": p["route"],
                "predicted_time": p["time"],
                "predicted_distance": p["distance"],
                "stats": stats,
            })
    finally:
        session.close()

    return result


@app.post("/trip")
def add_trip(trip: TripIn):
    """Записать поездку в БД."""
    session = get_session()
    try:
        r = Route(
            start_point=trip.start_point,
            finish_point=trip.finish_point,
            route=trip.route,
            time=trip.time,
            distance=trip.distance,
            actual_time=trip.actual_time,
            actual_distance=trip.actual_distance,
            traffic=trip.traffic,
            difficulty=trip.difficulty,
        )
        session.add(r)
        session.commit()
        session.refresh(r)
        return {"id": r.id, "status": "saved"}
    finally:
        session.close()


@app.get("/history")
def history(route: str):
    """История поездок по маршруту 'A,C,F,G'."""
    session = get_session()
    try:
        trips = get_trips_by_route(session, route)
        return [
            {
                "id": t.id,
                "start_point": t.start_point,
                "finish_point": t.finish_point,
                "route": t.route,
                "time": t.time,
                "distance": t.distance,
                "actual_time": t.actual_time,
                "actual_distance": t.actual_distance,
                "traffic": t.traffic,
                "difficulty": t.difficulty,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in trips
        ]
    finally:
        session.close()


@app.get("/recommend")
def rec(start: str, finish: str):
    """AI-рекомендация по направлению."""
    session = get_session()
    try:
        result = recommend(session, start, finish)
        if result is None:
            return {"recommendation": None, "reason": "нет данных по направлению"}
        return result
    finally:
        session.close()


@app.get("/analyze")
def ana(route: str):
    """AI-анализ прогноза по маршруту."""
    session = get_session()
    try:
        return {"analysis": analyze(session, route)}
    finally:
        session.close()


@app.get("/stats")
def stats():
    """Топ маршрутов."""
    session = get_session()
    try:
        return popular_routes(session)
    finally:
        session.close()