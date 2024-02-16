import math
import random
import string
import time
from collections import Counter

from unidecode import unidecode

from utils.constants.labels import EXEC_TIME, FREQ, APPROX_CNT, DS_CNT
from utils.constants.parameters import A


class Solution:

    def __init__(self, counter: dict, execution_time):
        self.counter = counter
        self.execution_time = execution_time

    def list_counter(self):
        return [(k, v) for k, v in self.counter.items()]

    def to_json(self):
        return {FREQ: self.list_counter(), EXEC_TIME: self.execution_time}


def exact_counter(stream) -> Solution:
    start = time.time()
    counter = dict()
    for char in stream:
        if char not in counter:
            counter[char] = 0
        counter[char] += 1
    execution_time = time.time() - start

    return Solution(counter, execution_time)


def approximate_counter(stream) -> Solution:
    counter = dict()
    start = time.time()
    for char in stream:
        if char not in counter:
            counter[char] = 0

        # Increment based on probability
        if random.uniform(0, 1) <= decreasing_probability(A, counter[char]):
            counter[char] += 1

    execution_time = time.time() - start
    return Solution(counter, execution_time)


def data_stream_counter(stream, k) -> Solution:
    counter = dict()
    start = time.time()
    for char in stream:
        if char in counter:
            counter[char] += 1
        elif len(counter) < k - 1:
            counter[char] = 1
        else:
            # Decrement all counters
            for key in counter:
                counter[key] -= 1
            # Remove items with 0 size
            counter = {k: v for k, v in counter.items() if v != 0}
    execution_time = time.time() - start
    return Solution(counter, execution_time)


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
    text = unidecode(text)

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


def analyse(exact_count, approx_count_list, data_stream_count, k_list):
    statistics = {
        DS_CNT: analyse_data_stream_counter(exact_count, data_stream_count),
        APPROX_CNT: analyse_approximate_counter(exact_count, approx_count_list, k_list),
    }
    return statistics


def analyse_approximate_counter(exact_solution, approx_solution, k_list):
    if 1 not in k_list:
        k_list.append(1)

    # Real order
    exact_ordered_counter = sorted([(k, v) for k, v in exact_solution.items()], key=lambda x: (-x[1], x[0]))
    exact_order = "".join([i[0] for i in exact_ordered_counter])

    # Total number of counted characters per trial (For n trials)
    approx_n_list = list()
    # Character count for all trials
    char_count = dict()
    # Total types of orders for all the trials and its count
    total_orders = dict()
    # total types of k most frequent chars for all the trials and its count
    k_most_frequent = {k: dict() for k in k_list}

    for cur_counter in approx_solution:
        ordered_counter = sorted([(k, v) for k, v in cur_counter.items()], key=lambda x: (-x[1], x[0]))
        cur_order = "".join([i[0] for i in ordered_counter])

        # total chars counter per trial
        approx_n_list.append(sum(cur_counter.values()))

        # Char count
        for char in cur_counter:
            if char not in char_count:
                char_count[char] = list()
            char_count[char].append(cur_counter[char])

        # total orders
        if cur_order not in total_orders:
            total_orders[cur_order] = 0
        total_orders[cur_order] += 1

        # k most frequent
        for k in k_list:
            k_cur_order = cur_order[:k]
            if k_cur_order not in k_most_frequent[k]:
                k_most_frequent[k][k_cur_order] = 0
            k_most_frequent[k][k_cur_order] += 1

    # Order Accuracy
    order_accuracy = get_accuracy(exact_order, total_orders)
    k_order_accuracy = {k: get_accuracy(exact_order[:k], k_most_frequent[k]) for k in k_list}

    # Average approximate counter
    avg_approx_counter = {char: math.floor(get_mean(count)) for char, count in char_count.items()}

    # Expected approximate counter
    expected_approx_counter = {k: expected_value_by_decreasing_probability(2, v)
                               for k, v in exact_solution.items()}

    # number of events(Number of characters in the text)
    expected_n = sum(expected_approx_counter.values())
    real_n = sum(exact_solution.values())

    # Real Variance
    real_variance = expected_n / 2
    # Real standard deviation
    real_standard_deviation = math.sqrt(real_variance)
    n = len(approx_n_list)
    # Mean
    mean = get_mean(approx_n_list)
    # Maximum deviation
    maximum_deviation = max([abs(total - mean) for total in approx_n_list])
    # Mean absolute deviation
    mean_absolute_deviation = sum([abs(total - mean) for total in approx_n_list]) / n
    # Variance
    variance = sum([(count - mean) ** 2 for count in approx_n_list]) / n
    # Standard deviation (variance ** 0.5)
    standard_deviation = math.sqrt(sum([(count - mean) ** 2 for count in approx_n_list]) / n)
    # Mean absolute error
    mean_absolute_error = sum([abs(count - real_n) for count in approx_n_list]) / n
    # Mean relative error
    mean_relative_error = sum([abs(count - real_n) / real_n * 100 for count in approx_n_list]) / n
    # Mean get_accuracy ratio
    mean_accuracy_ratio = mean / expected_n
    # Smallest counter value
    smallest_value = min(approx_n_list)
    # Largest counter value
    largest_value = max(approx_n_list)

    statistics = {
        "avg_approx_counter": avg_approx_counter,
        "order_accuracy": order_accuracy, "k_order_accuracy": k_order_accuracy,
        "real_variance": real_variance, "real_standard_deviation": real_standard_deviation,
        "mean_absolute_error": mean_absolute_error, "mean_relative_error": mean_relative_error,
        "mean_accuracy_ratio": mean_accuracy_ratio, "smallest_value": smallest_value, "largest_value": largest_value,
        "mean": mean, "mean_absolute_deviation": mean_absolute_deviation, "standard_deviation": standard_deviation,
        "maximum_deviation": maximum_deviation, "variance": variance,
        "k_most_frequent": k_most_frequent, "total_orders": total_orders,
    }
    return statistics


def analyse_data_stream_counter(exact_solution, ds_solution):
    # Real order
    exact_order = get_order(exact_solution)

    statistics = dict()

    for k in ds_solution:
        cur_order = get_order(ds_solution[k])

        k_exact_order = exact_order[:len(ds_solution[k])]

        accurate_chars = [char for char in cur_order if char in k_exact_order]
        accuracy = round(len(accurate_chars) / (int(k) - 1), 4)

        statistics[k] = {
            "order": cur_order, "accurate_chars": accurate_chars, "accuracy": accuracy
        }
    return statistics


def get_accuracy(x, dictionary):
    return dictionary[x] / sum(dictionary.values()) if x in dictionary else 0


def get_order(counter: dict):
    ordered_counter = sorted([(k, v) for k, v in counter.items()], key=lambda x: (-x[1], x[0]))
    order = "".join([i[0] for i in ordered_counter])
    return order


def analyse_text_in_different_languages(exact_counter_list, k_list):
    if 1 not in k_list:
        k_list = [1] + k_list
    exact_order_list = {k: get_order(v) for k, v in exact_counter_list.items()}

    k_most_frequent = {k: dict() for k in k_list}
    for k in k_list:
        for title in exact_order_list:
            k_most_frequent[k][title] = exact_order_list[title][:k]
    return k_most_frequent


def decreasing_probability(a, k):
    return 1 / (a ** k)


def expected_value_by_decreasing_probability(a, k):
    return math.floor(math.log(k * (a - 1) + a - 1) / math.log(a))


def experiment_approximate_counter(stream, n_trials):
    approx_solutions = [approximate_counter(stream) for _ in range(n_trials)]
    return {EXEC_TIME: get_mean([i.execution_time for i in approx_solutions]),
            FREQ: [i.counter for i in approx_solutions]}


def experiment_data_stream_counter(stream, k_list):
    return {k: data_stream_counter(stream, k).to_json() for k in k_list}


def get_mean(lst: list):
    from statistics import mean
    return mean(lst)
