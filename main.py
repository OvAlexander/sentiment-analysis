import graph
from common import LOGGING, DATES, NUM_DATES, NUM_TEAMS, CHAT_PATH, GRAPH_PATH
# (\d{1,3}|\d{1,3}\.\d{1,3})\/\d{1,3}


def log(*args, **kwargs):
    if LOGGING:
        print(*args, **kwargs)


if __name__ == "__main__":
    graph.graph_by_team()
    graph.graph_all(True)
    graph.graph_all(False)
