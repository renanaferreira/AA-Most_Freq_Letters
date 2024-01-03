import string
from collections import Counter
from statistics import mean
from unidecode import unidecode

from utils.constants.labels import EXEC_TIME, FREQ, APPROX_CNT


def get_language(filepath):
    try:
        with open(filepath, 'r', encoding="utf8") as fp:
            language_line = [line for line in fp if "Language:" in line]

        # Format line
        language = language_line[0].strip().split(":")[1].strip().lower()
        return language
    except:
        raise Exception("Illegal Argument! All Gutenberg books must have a header signaling the book's language.")


def get_title(filepath):
    try:
        with open(filepath, 'r', encoding="utf8") as fp:
            title_line = [line for line in fp if "Title:" in line]

        title = title_line[0].strip().split(":")[1].strip().split()
        title = [word.lower() for word in title]
        title = "_".join(title)

        return title
    except:
        raise Exception("Illegal Argument! All Gutenberg books must have a header signaling the book's title.")


def process_text(stream, stopwords):
    # remove header & footer
    text = stream.split("***")[2]

    # remove punctuation
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)

    # Remove stopwords
    text = "".join([word.upper() for word in text.split() if word.lower() not in stopwords])

    # Remove numerical characters
    text = "".join([char for char in text if char.isalpha()])

    # Replace accented characters by ascii similar
    print(text)
    text = unidecode(text)
    print(text)
    exit()

    return text


def get_words_frequency(text):
    # remove header & footer
    text = text.split("***")[2]

    # remove punctuation
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)

    # Get words lower
    words = [word.lower() for word in text.split()]

    # Get counter
    counter = dict(Counter(words))
    counter = [(k, v) for k, v in counter.items()]
    counter.sort(reverse=True, key=lambda x: x[1])

    return counter


def analyse(exact_counter_solution, approx_counter_solution, data_stream_solution):
    statistics = dict()

    statistics[APPROX_CNT] = analyse_approximate_counter(exact_counter_solution, approx_counter_solution)

    # get average time in approximate counter trials
    exec_times = [item[EXEC_TIME] for item in approx_counter_solution]
    approx_counter_sol_avg_exec_time = mean(exec_times)

    return statistics


def analyse_approximate_counter(exact_solution, approx_solution):
    # Total number of counted characters per trial (For n trials)
    total_chars_per_trial = [sum(trial[FREQ].values()) for trial in approx_solution]

    # Character count for all trials
    char_count = dict()
    # Total types of orders for all the trials
    total_orders = set()

    for trial in approx_solution:
        cur_counter = trial[FREQ]

        # Char count
        for char in cur_counter:
            if char not in char_count:
                char_count[char] = list()
            char_count[char].append(cur_counter[char])

        # total orders
        ordered_counter = sorted([(k, v) for k, v in cur_counter.items()], key=lambda x: (-x[1], x[0]))
        cur_order = "".join([i[0] for i in ordered_counter])
        print(ordered_counter)
        print(cur_order)
        exit()

    # Keep track of order for first 3 letters
    first_3_letters = {}

    # Keep track of most frequent letter
    most_frequent_letters = {}

    return total_orders
