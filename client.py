"""
client.py
---------
"""

import requests


BASE_URL = "http://127.0.0.1:8000"


def get_routes(start, finish):
    """Возможные маршруты + статистика."""
    r = requests.get(f"{BASE_URL}/routes", params={"start": start, "finish": finish})
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()


def add_trip(data):
    """Записать поездку."""
    r = requests.post(f"{BASE_URL}/trip", json=data)
    r.raise_for_status()
    return r.json()


def get_history(route):
    """История поездок по маршруту 'A,C,F,G'."""
    r = requests.get(f"{BASE_URL}/history", params={"route": route})
    r.raise_for_status()
    return r.json()


def get_recommendation(start, finish):
    """AI-рекомендация по направлению."""
    r = requests.get(f"{BASE_URL}/recommend", params={"start": start, "finish": finish})
    r.raise_for_status()
    return r.json()


def get_analysis(route):
    """AI-анализ прогноза по маршруту."""
    r = requests.get(f"{BASE_URL}/analyze", params={"route": route})
    r.raise_for_status()
    return r.json()


def get_stats():
    """Топ маршрутов."""
    r = requests.get(f"{BASE_URL}/stats")
    r.raise_for_status()
    return r.json()


def health():
    """Проверка, что сервер жив."""
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=2)
        return r.status_code == 200
    except requests.RequestException:
        return False