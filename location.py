#  указываться в time distance но не в actual time/distance
GRAPH = {
    "A": {
        "B": {"distance": 5, "time": 10},
        "C": {"distance": 7, "time": 12},
    },
    "B": {
        "A": {"distance": 5, "time": 10},
        "D": {"distance": 6, "time": 11},
        "E": {"distance": 8, "time": 14},
    },
    "C": {
        "A": {"distance": 7, "time": 12},
        "F": {"distance": 9, "time": 15},
    },
    "D": {
        "B": {"distance": 6, "time": 11},
        "E": {"distance": 4, "time": 8},
        "F": {"distance": 5, "time": 9},
    },
    "E": {
        "B": {"distance": 8, "time": 14},
        "D": {"distance": 4, "time": 8},
        "G": {"distance": 10, "time": 18},
    },
    "F": {
        "C": {"distance": 9, "time": 15},
        "D": {"distance": 5, "time": 9},
        "G": {"distance": 7, "time": 12},
    },
    "G": {
        "E": {"distance": 10, "time": 18},
        "F": {"distance": 7, "time": 12},
    },
}