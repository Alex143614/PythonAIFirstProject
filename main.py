"""
main.py
"""

from client import (
    health,
    get_routes,
    add_trip,
    get_history,
    get_analysis,
)


selected = None


def ask(prompt):
    return input(prompt).strip()


def line():
    print("-" * 50)


def check_server():
    if not health():
        print("Сервер не запущен. Запустите:")
        print("  venv/bin/uvicorn api:app --reload")
        return False
    return True


def menu_choose_route():
    global selected

    start = ask("Начальная точка: ").upper()
    finish = ask("Конечная точка: ").upper()

    routes = get_routes(start, finish)
    if not routes:
        print(f"Путей {start} -> {finish} не найдено.")
        return

    print()
    print(f"Возможные маршруты {start} -> {finish}:")
    for i, r in enumerate(routes, 1):
        path = " -> ".join(r["route_list"])
        print()
        print(f"  [{i}] {path}")
        print(f"      Прогноз: {r['predicted_time']} мин, {r['predicted_distance']} км")
        st = r["stats"]
        if st:
            print(f"      Факт: {round(st['avg_actual_time'], 1)} мин, "
                  f"{round(st['avg_actual_distance'], 1)} км ({st['count']} поездок)")
        else:
            print("      Факт: нет данных")

    idx = ask("\nВыберите номер (Enter — отмена): ")
    if not idx.isdigit() or not (1 <= int(idx) <= len(routes)):
        print("Отменено.")
        return

    selected = routes[int(idx) - 1]
    route_str = selected["route"]

    print()
    line()
    print(f"Маршрут {route_str}")
    print(f"Прогноз: {selected['predicted_time']} мин, "
          f"{selected['predicted_distance']} км")

    st = selected["stats"]
    if st:
        print(f"Факт: среднее {round(st['avg_actual_time'], 1)} мин, "
              f"min {st['min_time']}, max {st['max_time']}")
        print(f"Дистанция: среднее {round(st['avg_actual_distance'], 1)} км, "
              f"min {st['min_distance']}, max {st['max_distance']}")
        print(f"Поездок: {st['count']}")
        analysis = get_analysis(route_str)
        print(f"AI: {analysis['analysis']}")
    else:
        print("Факт: нет данных")
    line()


def menu_add_trip():
    global selected

    if selected is None:
        print("Сначала выберите путь (пункт 1).")
        return

    route_str = selected["route"]
    print(f"Поездка по маршруту {route_str}")

    actual_time = ask("Фактическое время (мин): ")
    actual_distance = ask("Фактическая дистанция (км): ")
    traffic = ask("Трафик (1-3): ")
    difficulty = ask("Сложность (1-3): ")

    if not all(x.isdigit() for x in [actual_time, actual_distance, traffic, difficulty]):
        print("Нужны числа. Отменено.")
        return

    data = {
        "start_point": selected["route_list"][0],
        "finish_point": selected["route_list"][-1],
        "route": route_str,
        "time": selected["predicted_time"],
        "distance": selected["predicted_distance"],
        "actual_time": int(actual_time),
        "actual_distance": int(actual_distance),
        "traffic": int(traffic),
        "difficulty": int(difficulty),
    }

    result = add_trip(data)
    print(f"Сохранено (id={result['id']})")


def menu_history():
    route_str = ask("Маршрут (например A,C,F,G): ").upper()

    trips = get_history(route_str)
    if not trips:
        print("Поездок по этому маршруту нет.")
        return

    print()
    print(f"Поездки по маршруту {route_str}:")
    print(f"{'N':<4}{'время':<8}{'дист':<8}{'трафик':<9}{'сложн':<8}{'дата':<20}")
    line()

    for i, t in enumerate(trips, 1):
        print(f"{i:<4}{t['actual_time']:<8}{t['actual_distance']:<8}"
              f"{t['traffic']:<9}{t['difficulty']:<8}{t['created_at'][:16]:<20}")

    line()
    times = [t["actual_time"] for t in trips]
    dists = [t["actual_distance"] for t in trips]
    print(f"Быстрейшая: {min(times)} мин")
    print(f"Медленнейшая: {max(times)} мин")
    print(f"Короткая: {min(dists)} км")
    print(f"Длинная: {max(dists)} км")
    def show_menu():
    print()
    print("===== AI NAVIGATOR =====")
    print("1. Выбрать путь")
    print("2. Создать поездку")
    print("3. Показать поездки по маршруту")
    print("0. Выход")


def main():
    if not check_server():
        return

    while True:
        show_menu()
        choice = ask("Выбор: ")

        if choice == "1":
            menu_choose_route()
        elif choice == "2":
            menu_add_trip()
        elif choice == "3":
            menu_history()
        elif choice == "0":
            print("Пока!")
            break
        else:
            print("Неверный выбор.")


if name == "main":
    main()