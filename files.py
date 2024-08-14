from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import os
import calc


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
    pattern = r"(\d{1,3}|\d{1,3}\.\d{1,3})\/\d{1,3})"
    pattern2 = r"(\d{1,3} out of \d{1,3})|(\d{1,3}\.\d{1,3} out of \d{1,3})"
    scores = []
    dates = []
    for text in text_chunk:
        date = text[-12:-1]
        if re.search(pattern=pattern, string=text) or re.search(pattern=pattern2, string=text):
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
    pattern2 = r"(\d{1,3} out of \d{1,3}|\d{1,3}\.\d{1,3} out of \d{1,3})"
    scores = []
    dates = []
    analyzer = SentimentIntensityAnalyzer()
    for sentence in text_chunk:
        date = sentence[-12:-1]
        if re.search(pattern=pattern, string=sentence) or re.search(pattern=pattern2, string=sentence):
            if re.search(pattern=pattern, string=sentence):
                score = float(re.findall(pattern=pattern,
                                         string=sentence)[0])
            else:
                score = float(re.findall(pattern=pattern2,
                                         string=sentence)[0][0:2])
            if date in dates:
                scores[len(scores)-1] = (scores[len(scores)-1] + score)/2
            else:
                scores.append(score)
                dates.append(date)
        else:
            score = analyzer.polarity_scores(sentence)
            remapped_score = calc.scale(score["compound"], -1.0, 1.0, 0, 10)
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


def gather_file_names(directory_path):
    """Gathers file names from a given directory.

    Args:
      directory_path: The path to the directory to scan.

    Returns:
      A list of file names within the directory.
    """

    file_names = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension == ".txt":
                file_names.append(file)
    return file_names
