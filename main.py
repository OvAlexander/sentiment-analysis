from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import re


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
analyzer = SentimentIntensityAnalyzer()
sentence_analysis = []

chat_log = parse_text("chat_logs\general_redpanda9347.txt")
count = 0
for i, sentence in enumerate(chat_log):
    date = sentence[-12:]
    vs = analyzer.polarity_scores(sentence)
    # if chat_log[i+1][-12:] == date:
    #     # Check if the next sentece has the same date then add later
    #     sentence_analysis
    #     count += 1
    # else:
    sentence_analysis.append(vs)
    # print("{:-<65} {}".format(sentence, str(vs)))


data_points = []

for sentence in sentence_analysis:
    print(sentence["compound"])
    data_points.append(sentence["compound"])

print(np.arange(1, len(data_points)+1, 1, dtype=int))

print("#$#$#"*20)
print(chat_log)

graph(np.arange(1, len(data_points)+1, 1, dtype=int), data_points)
