import random
import time
from collections import Counter
import numpy as np

from utils.constants.labels import FREQ, EXEC_TIME


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
    counter = dict(Counter(stream))
    execution_time = time.time() - start

    return Solution(counter, execution_time)


def approximate_counter(stream) -> Solution:
    counter = dict()
    start = time.time()
    for char in stream:
        if char not in counter:
            counter[char] = 0

        # Decrease probability
        k_factor = counter[char]
        probability = 1 / pow(np.array([2]), k_factor)

        # Increment based on probability
        if np.random.uniform(0, 1) <= probability:
            counter[char] += 1

    execution_time = time.time() - start
    return Solution(counter, execution_time)


def data_stream_counter(stream, k) -> Solution:
    counter = dict()
    start = time.time()
    for char in stream:
        if char in counter:
            counter[char] += 1
        else:
            if len(counter) < k - 1:
                counter[char] = 1
            else:
                # Decrement all counters
                for key in counter:
                    counter[key] -= 1
                # Remove items with 0 length
                counter = {k: v for k, v in counter.items() if v != 0}
    execution_time = time.time() - start
    return Solution(counter, execution_time)
