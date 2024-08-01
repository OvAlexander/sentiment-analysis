from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import re
import os
# (\d{1,3}|\d{1,3}\.\d{1,3})\/\d{1,3}
LOGGING = False
DATES = ['Jul  8 2024', 'Jul  9 2024', 'Jul 10 2024', 'Jul 11 2024', 'Jul 12 2024',
         'Jul 15 2024', 'Jul 16 2024', 'Jul 17 2024', 'Jul 18 2024', 'Jul 19 2024',
         'Jul 22 2024', 'Jul 23 2024', 'Jul 24 2024', 'Jul 25 2024', 'Jul 26 2024',
         'Jul 29 2024', 'Jul 30 2024']
# , 'Jul 31 2024', 'Aug  1 2024', 'Aug  2 2024',
#          'Aug  3 2024', 'Aug  4 2024']


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


def scale(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


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
    plt.grid(color='c', linestyle='--', linewidth=0.5)

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
    plt.yticks(np.arange(0, 11))
    plt.ylim(0, 10)

    # Creates a line displaying neutral
    plt.hlines(5, 0, max(x))
    plt.grid(color='c', linestyle='--', linewidth=0.25)

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
    file = open(file_name, "r", encoding="utf-8")

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
    analyzer = SentimentIntensityAnalyzer()
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


def mixed_entry(text_chunk: list):
    pattern = r"(\d{1,3}|\d{1,3}\.\d{1,3})\/\d{1,3}"
    scores = []
    dates = []
    analyzer = SentimentIntensityAnalyzer()
    for sentence in text_chunk:
        date = sentence[-12:-1]
        if re.search(pattern=pattern, string=sentence):
            score = float(re.findall(pattern=pattern,
                                     string=sentence)[0])
            if date in dates:
                scores[len(scores)-1] = (scores[len(scores)-1] + score)/2
            else:
                scores.append(score)
                dates.append(date)
        else:
            score = analyzer.polarity_scores(sentence)
            remapped_score = scale(score["compound"], -1.0, 1.0, 0, 10)
            if date in dates:
                scores[len(scores)-1] = (scores[len(scores)-1] +
                                         remapped_score)/2
            else:
                scores.append(remapped_score)
                dates.append(date)
    print(scores)
    print(dates)
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


def interp(data: list, days: list) -> list:
    days_with_data = []

    # data = [7.0, 5.0, None, 1.0, None, None, None,
    #         9.0, 6.0, None, None, None, None, 7.0]
    interp_data = []
    for date in DATES:
        if date in days:
            days_with_data.append(True)
        else:
            days_with_data.append(False)
            pos = DATES.index(date)
            data.insert(pos, None)

    i = 0
    while i < len(days_with_data):
        dd = days_with_data[i]
        if (i == 0 or i == len(days_with_data) - 1) and dd == 0:
            raise ValueError('Cannot interpolate because of undefined bounds')

        if dd == False:
            # Find index bounds to lerp
            first = i - 1
            remaining = days_with_data[i:]
            last = remaining.index(True) + i
            n_steps = last - first - 1

            # Compute lerp
            # 2 to account for start and end, then cut off start and end
            pts = np.linspace(data[first], data[last],
                              n_steps + 2)[1:n_steps + 1]
            interp_data += list(pts)

            # Set i to last index
            i = last - 1

        else:
            interp_data += [data[i]]
        i += 1
    return interp_data


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


chat_log = parse_text("bwsi_logs/yuno-n_agentn_.txt")
chat_log2 = parse_text("bwsi_logs/ajay-g_ajaytastic.txt")
chat_log3 = parse_text("bwsi_logs/jacqueline-t_dear_jacquelineee0905.txt")
chat_log4 = parse_text("bwsi_logs/victoria-g_ocurien.txt")
chat_log5 = parse_text("bwsi_logs/jeffrey-t_jefft72.txt")

chat_log.pop(0)
chat_log2.pop(0)
chat_log3.pop(0)
chat_log4.pop(0)
chat_log5.pop(0)

# Chat log 3
score, date = mixed_entry(chat_log3)
score, date = mixed_entry(chat_log4)
score, date = mixed_entry(chat_log5)


# # Chat log 2
# chat_scores, chat_scores_dates = scan_for_scores(chat_log2)

# chat_scores.reverse()
# chat_scores_dates.reverse()
# # Chat Log 1
# scores = analyze_text(chat_log)

# compound_scores = get_compound(scores)
# dates = get_dates(scores)

# compound_scores.reverse()
# dates.reverse()

# num_scores = np.arange(1, len(compound_scores)+1, 1, dtype=int)

# graph(dates, compound_scores)
# graph_scores(chat_scores_dates, chat_scores)

date.reverse()
score.reverse()
new_score = interp(score, date)
print("LOOOOK HERE")
print(new_score)
print(DATES)
graph_scores(DATES, new_score)
