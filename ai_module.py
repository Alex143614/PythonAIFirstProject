"""
ai_module.py
"""

from statistics import prediction_diff, points_stats, route_stats


MIN_TRIPS = 3          
SIGNIFICANT_PERCENT = 10  


def analyze(session, route_str):
    diff = prediction_diff(session, route_str)

    if diff is None:
        return f"Маршрут {route_str}: нет данных."

    if diff["count"] < MIN_TRIPS:
        return f"Маршрут {route_str}: мало данных ({diff['count']} поездок)."

    p = diff["percent_time"]
    if abs(p) < SIGNIFICANT_PERCENT:
        return f"Маршрут {route_str}: прогноз точный (отклонение {p}%)."

    if p > 0:
        return (f"Маршрут {route_str}: прогноз занижает время "
                f"на {p}% ({diff['diff_time']} мин в среднем).")
    else:
        return (f"Маршрут {route_str}: прогноз завышает время "
                f"на {abs(p)}% ({abs(diff['diff_time'])} мин в среднем).")


def recommend(session, start, finish):
    stats_list = points_stats(session, start, finish)
    if not stats_list:
        return None

    # фильтруем маршруты, по которым есть хоть какие-то данные
    valid = [s for s in stats_list if s["stats"]["count"] >= 1]
    if not valid:
        return None

    # сортируем по среднему ФАКТИЧЕСКОМУ времени
    valid.sort(key=lambda x: x["stats"]["avg_actual_time"])
    best = valid[0]

    reason = f"среднее фактическое время: {round(best['stats']['avg_actual_time'], 1)} мин"

    # если есть второй вариант — сравним
    if len(valid) > 1:
        second = valid[1]
        delta = round(second["stats"]["avg_actual_time"] - best["stats"]["avg_actual_time"], 1)
        if delta > 0:
            reason = f"быстрее на {delta} мин, чем альтернатива"

    return {
        "route": best["route"],
        "reason": reason,
        "stats": best["stats"],
    }