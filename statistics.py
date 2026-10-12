"""
statistics.py
"""

from sqlalchemy import func
from db import Route


def get_trips_by_route(session, route_str):
    return session.query(Route).filter(Route.route == route_str).all()


def get_trips_by_points(session, start, finish):
    return (
        session.query(Route)
        .filter(Route.start_point == start, Route.finish_point == finish)
        .all()
    )


def route_stats(session, route_str):
    trips = get_trips_by_route(session, route_str)
    if not trips:
        return None

    times = [t.actual_time for t in trips]
    dists = [t.actual_distance for t in trips]

    return {
        "count": len(trips),
        "avg_time": sum(t.time for t in trips) / len(trips),
        "avg_distance": sum(t.distance for t in trips) / len(trips),
        "min_time": min(times),
        "max_time": max(times),
        "min_distance": min(dists),
        "max_distance": max(dists),
        "avg_actual_time": sum(times) / len(trips),
        "avg_actual_distance": sum(dists) / len(trips),
    }


def points_stats(session, start, finish):
    trips = get_trips_by_points(session, start, finish)
    if not trips:
        return []

    result = []
    for r in set(t.route for t in trips):
        stats = route_stats(session, r)
        if stats:
            result.append({"route": r, "stats": stats})
    return result


def prediction_diff(session, route_str):
    trips = get_trips_by_route(session, route_str)
    if not trips:
        return None

    n = len(trips)
    avg_pred_t = sum(t.time for t in trips) / n
    avg_pred_d = sum(t.distance for t in trips) / n
    avg_act_t = sum(t.actual_time for t in trips) / n
    avg_act_d = sum(t.actual_distance for t in trips) / n

    return {
        "count": n,
        "diff_time": round(avg_act_t - avg_pred_t, 1),
        "diff_distance": round(avg_act_d - avg_pred_d, 1),
        "percent_time": round((avg_act_t - avg_pred_t) / avg_pred_t * 100, 1),
        "percent_distance": round((avg_act_d - avg_pred_d) / avg_pred_d * 100, 1),
    }


def popular_routes(session, limit=10):
    rows = (
        session.query(Route.route, func.count(Route.id))
        .group_by(Route.route)
        .order_by(func.count(Route.id).desc())
        .limit(limit)
        .all()
    )
    return [{"route": r, "count": c} for r, c in rows]