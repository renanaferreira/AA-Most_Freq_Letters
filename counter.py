import argparse
import json
import os
import random

from utils.constants.labels import EXACT_CNT, APPROX_CNT, DS_CNT
from utils.constants.parameters import DIR_PROCESSED, SEED, N_TRIALS, K_LIST, DIR_SOL
from utils.counters import approximate_counter, exact_counter, data_stream_counter


def execute(dir_texts, dir_output, n_trials, k_list):
    if not os.path.exists(dir_texts):
        raise ValueError(f"Illegal Argument! {dir_texts} does not exist!")

    if not os.path.exists(dir_output):
        os.mkdir(dir_output)

    book_titles = [title for title in os.listdir(dir_texts) if title.endswith('.txt')]

    for book_title in book_titles:
        title = book_title.split(".")[0]
        statistics = dict()

        with open(os.path.join(dir_texts, book_title), "r", encoding="utf8") as fp_input:
            text = fp_input.read()

        text = text[:1000]
        # Exact counter
        exact_solution = exact_counter(text)
        statistics[EXACT_CNT] = exact_solution.to_json()

        # Approximate counter
        statistics[APPROX_CNT] = list()
        for trial in range(n_trials):
            solution = approximate_counter(text)
            statistics[APPROX_CNT].append(solution.to_json())

        # Data Stream counter
        statistics[DS_CNT] = dict()
        for k_factor in k_list:
            solution = data_stream_counter(text, k_factor)
            statistics[DS_CNT][k_factor] = solution.to_json()

        with open(os.path.join(dir_output, f"{title}.json"), "w", encoding="utf8") as fp_output:
            json.dump(statistics, fp_output, ensure_ascii=False)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Most Frequent Letters Count")
    parser.add_argument("--dir_texts", type=str, help="Directory with texts to count",
                        default=DIR_PROCESSED)
    parser.add_argument("--dir_output", type=str, help="Directory to store count solutions",
                        default=DIR_SOL)
    parser.add_argument("--seed", type=int, help="Seed for randomness",
                        default=SEED)
    parser.add_argument("--n_trials", type=int, help="Number of trials",
                        default=N_TRIALS)
    parser.add_argument("--k_list", type=int, help="List of K factor for data stream counting", nargs="+",
                        default=K_LIST)
    args = parser.parse_args()

    random.seed(args.seed)
    execute(args.dir_texts, args.dir_output, args.n_trials, args.k_list)
