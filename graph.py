from common import NUM_DATES, NUM_TEAMS
import matplotlib.pyplot as plt
import numpy as np
import calc
import files
from utilities import string_to_rgb


def graph(x, y):
    # Sets up plot
    plt.plot(x, y, linestyle='dashed', marker='o')
    plt.xlabel("Sentence Number")
    plt.ylabel("Sentiment")
    plt.title("Sentiment Analysis over Time")
    plt.margins(x=0, y=0)
    plt.xticks(x)

    plt.ylim(-1.00, 1.00)

    # Creates a line displaying neutral
    plt.hlines(0, 0, max(x))
    plt.grid(color='c', linestyle='--', linewidth=0.5)

    # Creates plot
    plt.show()


def graph_scores(x, y, file_name: str, monster: bool):
    # Sets up plot
    color = string_to_rgb(file_name)
    plt.plot(x, y, linestyle='dashed', marker='o', color=color)
    plt.xlabel("Sentence Number")
    plt.ylabel("Sentiment")
    plt.title("Sentiment Analysis over Time")
    plt.margins(x=0, y=0)
    plt.xticks(x, rotation=45, ha='right')
    plt.yticks(np.arange(0, 11))
    plt.ylim(0, 10)

    # Creates a line displaying neutral
    plt.hlines(5, 0, max(x))
    plt.grid(color='c', linestyle='--', linewidth=0.25)

    # Creates plot
    plt.savefig(file_name)
    if monster:
        pass
    else:
        plt.clf()


def graph_dates(x, y):
    # Sets up plot
    plt.plot(x, y, linestyle='dashed', marker='o')
    plt.xlabel("Sentence Number")
    plt.ylabel("Sentiment")
    plt.title("Sentiment Analysis over Time")
    plt.margins(x=0, y=0)
    plt.xticks(x)
    plt.ylim(-1.00, 1.00)

    # Creates a line displaying neutral
    plt.hlines(0, 1, max(x))

    # Creates plot
    plt.show()


def graph_all(monster: bool):
    student_logs = files.gather_file_names("bwsi_logs")
    total_data = []
    count = 0
    for text_files in student_logs:
        print(f"Trying to plot {text_files}")
        chat_log = files.parse_text(f"bwsi_logs_parsed/{text_files}")
        chat_log.pop(0)
        score, date = files.mixed_entry(chat_log)

        date.reverse()
        score.reverse()
        new_score = calc.interp(score, date)
        if count == 0:
            total_data = new_score
        else:
            total_data = list(np.array(total_data) + np.array(new_score))
        graph_filename = "./new_bwsi_graphs/"+text_files[:-2]+"_graph.png"
        graph_scores(NUM_DATES, new_score, graph_filename, monster)
        count += 1

    for i in range(len(total_data)):
        total_data[i] *= 1.0/count

    if monster:
        graph_filename = "./new_bwsi_graphs/monster_graph.png"
    else:
        graph_filename = "./new_bwsi_graphs/total_avg_graph.png"
    graph_scores(NUM_DATES, total_data, graph_filename, monster)


def graph_by_team():
    for i in range(NUM_TEAMS):
        count = 0
        total_data = 0
        directory_path = f"./teams/team_{i+1}"
        chat_logs = files.gather_file_names(directory_path)
        for text_files in chat_logs:
            print(f"Trying to plot {text_files}")
            chat_log_path = directory_path + "/" + text_files
            chat_log = files.parse_text(chat_log_path)
            chat_log.pop(0)
            score, date = files.mixed_entry(chat_log)
            date.reverse()
            score.reverse()
            new_score = calc.interp(score, date)
            if count == 0:
                total_data = new_score
            else:
                total_data = list(np.array(total_data) + np.array(new_score))
            graph_filename = f"./teams/team_{i+1}/graphs/" + \
                text_files[:-2]+"_graph.png"
            graph_scores(NUM_DATES, new_score, graph_filename, False)
            count += 1
        for j in range(len(total_data)):
            total_data[j] *= 1.0/count
        graph_filename = f"./teams/team_{i+1}/graphs/team_{i+1}_avg_graph.png"
        graph_scores(NUM_DATES, total_data, graph_filename, False)
