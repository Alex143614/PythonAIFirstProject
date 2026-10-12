"""
router.py
"""

import heapq

from location import GRAPH


def dijkstra(start: str, finish: str, weight: str = "time") -> dict | None:
    if start not in GRAPH or finish not in GRAPH:
        return None

    # Минимальный вес до каждой вершины
    distances = {node: float("inf") for node in GRAPH}
    distances[start] = 0

    # Откуда пришли в вершину (для восстановления пути)
    previous = {node: None for node in GRAPH}

    # Приоритетная очередь: (вес, вершина)
    queue = [(0, start)]
    visited = set()

    while queue:
        current_weight, current_node = heapq.heappop(queue)

        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == finish:
            break

        for neighbor, edge in GRAPH[current_node].items():
            if neighbor in visited:
                continue

            new_weight = current_weight + edge[weight]

            if new_weight < distances[neighbor]:
                distances[neighbor] = new_weight
                previous[neighbor] = current_node
                heapq.heappush(queue, (new_weight, neighbor))

    if distances[finish] == float("inf"):
        return None

    # Восстанавливаем путь от finish к start, потом разворачиваем
    route = []
    node = finish
    while node is not None:
        route.append(node)
        node = previous[node]
    route.reverse()

    # Считаем суммарные distance и time по всему пути
    total_distance = 0
    total_time = 0
    for i in range(len(route) - 1):
        a, b = route[i], route[i + 1]
        edge = GRAPH[a][b]
        total_distance += edge["distance"]
        total_time += edge["time"]

    return {
        "route": route,
        "distance": total_distance,
        "time": total_time,
    }


# ============================================================
# ОБЁРТКИ
# ============================================================

def find_fastest_route(start: str, finish: str) -> dict | None:
    return dijkstra(start, finish, weight="time")


def find_shortest_route(start: str, finish: str) -> dict | None:
    return dijkstra(start, finish, weight="distance")


def find_routes(start: str, finish: str) -> list[dict]:
    routes = []
    seen = set()

    for r in (find_fastest_route(start, finish),
              find_shortest_route(start, finish)):
        if r is None:
            continue
        key = tuple(r["route"])
        if key not in seen:
            seen.add(key)
            routes.append(r)

    return routes

