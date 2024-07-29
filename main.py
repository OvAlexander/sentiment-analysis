from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import re

# (\d{1,3}|\d{1,3}\.\d{1,3})\/\d{1,3}
LOGGING = False


def log(*args, **kwargs):
    if LOGGING:
        print(*args, **kwargs)


def add_dicts(dict1, dict2):
    """Adds corresponding values of two dictionaries.

    Args:
      dict1: The first dictionary.
      dict2: The second dictionary.

    Returns:
      A new dictionary with the added values.
    """

    combined_dict = {key: dict1.get(key, 0) + dict2.get(key, 0)
                     for key in set(dict1) | set(dict2)}
    return combined_dict


def add_values_in_nested_lists(list_of_dicts):
    """Adds values in nested lists within dictionaries with the same keys.

    Args:
      list_of_dicts: A list of dictionaries.

    Returns:
      A new dictionary with summed values.
    """

    result = {}
    for d in list_of_dicts:
        for key, values in d.items():
            if key not in result:
                result[key] = [sum(x) for x in zip(*values)]
            else:
                for i in range(len(result[key])):
                    result[key][i] += values[i]
    return result


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

    # Creates plot
    plt.show()


def graph_scores(x, y):
    # Sets up plot
    plt.plot(x, y, linestyle='dashed', marker='o')
    plt.xlabel("Sentence Number")
    plt.ylabel("Sentiment")
    plt.title("Sentiment Analysis over Time")
    plt.margins(x=0, y=0)
    plt.xticks(x)

    plt.ylim(0, 10)

    # Creates a line displaying neutral
    plt.hlines(5, 0, max(x))

    # Creates plot
    plt.show()


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


def parse_text(file_name) -> list:
    parsed_text = []
    file = open(file_name, "r")

    "Thu Jul 18 15:07:49 2024"
    for line in file:
        if re.search(".:splitter:.", line) is not None:
            parsed_line = line.split(":splitter:")
            date = parsed_line[1][5:11] + parsed_line[1][20:54]
            parsed_line = parsed_line[0] + date
        else:
            parsed_line = line
        parsed_text.append(parsed_line)
    return parsed_text


def analyze_text(text_chunk: list):
    sentiment_scores = []
    analyzer = SentimentIntensityAnalyzer()
    for i, sentence in enumerate(text_chunk):
        date = sentence[-12:-1]
        vs = analyzer.polarity_scores(sentence)
        sentiment_scores.append(
            {date: [vs["neg"], vs["neu"], vs["pos"], vs["compound"]]})
        log("{:-<65} {}".format(sentence, str(vs)))
    return sentiment_scores


def scan_for_scores(text_chunk: list):
    pattern = r"(\d{1,3}|\d{1,3}\.\d{1,3})\/\d{1,3}"
    scores = []
    dates = []
    for text in text_chunk:
        date = text[-12:-1]
        if re.search(pattern=pattern, string=text):
            score = float(re.findall(pattern=pattern,
                                     string=text)[0])
            if date in dates:
                scores[len(scores)-1] = (scores[len(scores)-1] + score)/2
            else:
                scores.append(score)
                dates.append(date)
    return scores, dates


def get_compound(sentiment_scores: list):
    compound_score = []
    prev_date = 0
    for sentence in sentiment_scores:
        for date, score in sentence.items():
            if date == prev_date:
                compound_score[len(compound_score)-1] += score[3]
            else:
                compound_score.append(score[3])
            prev_date = date
    return compound_score


def get_dates(sentiment_scores: list):
    dates = []
    for sentence in sentiment_scores:
        if (isinstance(sentence, dict)):
            for date, score in sentence.items():
                if date not in dates:
                    dates.append(date)
        else:
            date = sentence[-12:-1]
            if date not in dates:
                dates.append(date)

    return dates


    # --- examples -------
sentences = ["VADER is smart, handsome, and funny.",  # positive sentence example
             # punctuation emphasis handled correctly (sentiment intensity adjusted)
             "VADER is smart, handsome, and funny!",
             # booster words handled correctly (sentiment intensity adjusted)
             "VADER is very smart, handsome, and funny.",
             "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
             # combination of signals - VADER appropriately adjusts intensity
             "VADER is VERY SMART, handsome, and FUNNY!!!",
             # booster words & punctuation make this close to ceiling for score
             "VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!",
             "VADER is not smart, handsome, nor funny.",  # negation sentence example
             "The book was good.",  # positive sentence
             # negated negative sentence with contraction
             "At least it isn't a horrible book.",
             # qualified positive sentence is handled correctly (intensity adjusted)
             "The book was only kind of good.",
             # mixed negation sentence
             "The plot was good, but the characters are uncompelling and the dialog is not great.",
             "Today SUX!",  # negative slang with capitalization emphasis
             # mixed sentiment example with slang and constrastive conjunction "but"
             "Today only kinda sux! But I'll get by, lol",
             "Make sure you :) or :D today!",  # emoticons handled
             "Catch utf-8 emoji such as such as 💘 and 💋 and 😁",  # emojis handled
             "Not bad at all"  # Capitalized negation
             ]

custom = ["Today was awful due to my code not working properly and barely getting anything done.",
          "Jackie and I worked on the weekly report slide.",
          "There were some flaws that I noticed later on.",
          "I should put in more details.",
          "I researched about finding slow-time data for RTI plot, and continued coding/researching all around the place.",
          "my schedule was a bit unorganized."
          ]


chat_log = parse_text("chat_logs\general_redpanda9347.txt")
chat_log2 = parse_text("chat_logs\merpymerp_redpanda9347.txt")

chat_log.pop(0)
chat_log2.pop(0)

chat_scores, chat_scores_dates = scan_for_scores(chat_log2)

chat_scores.reverse()
chat_scores_dates.reverse()

scores = analyze_text(chat_log)

compound_scores = get_compound(scores)
dates = get_dates(scores)

compound_scores.reverse()
dates.reverse()

num_scores = np.arange(1, len(compound_scores)+1, 1, dtype=int)

graph(dates, compound_scores)
graph_scores(chat_scores_dates, chat_scores)
