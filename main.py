from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import re


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
    plt.hlines(0, 1, max(x))

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
        date = sentence[-12:]
        vs = analyzer.polarity_scores(sentence)
        # if chat_log[i+1][-12:] == date:
        #     # Check if the next sentece has the same date then add later
        #     sentence_analysis
        #     count += 1
        # else:
        sentiment_scores.append(
            {date: [vs["neg"], vs["neu"], vs["pos"], vs["compound"]]})
        # print("{:-<65} {}".format(sentence, str(vs)))
    return sentiment_scores


def condense_scores(sentiment_scores: list):
    new_sentiment_scores = []
    len_scores = len(sentiment_scores)
    count = 0
    prev = {}
    # for i in range(len_scores):
    #     if scores[i][0] == scores[i+1][0]:
    #         scores[i][1] += scores[i+1][1]
    #         scores[i][2] += scores[i+1][2]
    #         scores[i][3] += scores[i+1][3]
    #         scores[i][4] += scores[i+1][4]
    #         sentiment_scores.pop(i+1)
    #         count += 1
    #         if i+1 == len_scores-count:
    #             break
    # print(sentiment_scores)


def get_compound(sentiment_scores: list):
    compound_score = []
    for sentence in sentiment_scores:
        compound_score.append(sentence[4])
    return compound_score

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
chat_log.pop(0)
scores = analyze_text(chat_log)
condense_scores(scores)
compound_scores = get_compound(scores)


dates = []
for sentence in chat_log:
    date = sentence[-12:]
    dates.append(date)


num_scores = np.arange(1, len(compound_scores)+1, 1, dtype=int)

# print("#$#$#"*20)
# print(chat_log)
# print(len(date))
# print(len(data_points))

# graph(num_scores, compound_scores)
