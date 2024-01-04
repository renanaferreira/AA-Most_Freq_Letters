import argparse
import json
import os
import random
import time

from utils.constants.labels import EXACT_CNT, APPROX_CNT, DS_CNT, EXEC_TIME, FREQ
from utils.constants.parameters import DIR_PROCESSED, SEED, N_TRIALS, K_LIST, DIR_SOL, DIR_EXEC_TIME
from utils.helpers import exact_counter, experiment_approximate_counter, experiment_data_stream_counter


def execute(dir_texts, dir_solutions, dir_exec_time, n_trials, k_list):
    if not os.path.exists(dir_texts):
        raise ValueError(f"Illegal Argument! {dir_texts} does not exist!")

    if not os.path.exists(dir_solutions):
        raise ValueError(f"Illegal Argument! {dir_solutions} does not exist!")

    if not os.path.exists(dir_exec_time):
        raise ValueError(f"Illegal Argument! {dir_exec_time} does not exist!")

    for book_title in [title for title in os.listdir(dir_texts) if title.endswith('.txt')]:
        with open(os.path.join(dir_texts, book_title), "r", encoding="utf8") as fp_input:
            text = fp_input.read()

        print(f"Count({book_title})")
        # Exact counter
        print(f"Exact count")
        exact_count = exact_counter(text).to_json()
        print(f"duration: {exact_count[EXEC_TIME]}s\n")
        # Approximate counter
        print(f"Approximate count")
        start = time.time()
        approx_count = experiment_approximate_counter(text, n_trials)
        duration = time.time() - start
        print(f"duration: {duration}s\n")
        # Data Stream counter
        print(f"Data stream count")
        start = time.time()
        ds_count = experiment_data_stream_counter(text, k_list)
        duration = time.time() - start
        print(f"duration: {duration}s\n")

        title = book_title.split(".")[0]

        # Store execution time
        exec_times = {EXACT_CNT: exact_count[EXEC_TIME],
                      APPROX_CNT: approx_count[EXEC_TIME],
                      DS_CNT: {k: ds_count[k][EXEC_TIME] for k in ds_count}}
        with open(os.path.join(dir_texts, f"{title}.json"), "w", encoding="utf8") as fp:
            json.dump(exec_times, fp, ensure_ascii=False)

        # Store solutions
        solutions = {EXACT_CNT: exact_count[FREQ],
                     APPROX_CNT: approx_count[FREQ],
                     DS_CNT: {k: ds_count[k][FREQ] for k in ds_count}}
        with open(os.path.join(dir_solutions, f"{title}.json"), "w", encoding="utf8") as fp:
            json.dump(solutions, fp, ensure_ascii=False)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Most Frequent Letters Count")
    parser.add_argument("--dir_texts", type=str, help="Directory with texts to count",
                        default=DIR_PROCESSED)
    parser.add_argument("--dir_solutions", type=str, help="Directory to store count solutions",
                        default=DIR_SOL)
    parser.add_argument("--dir_exec_time", type=str, help="Directory to store count solutions",
                        default=DIR_EXEC_TIME)
    parser.add_argument("--seed", type=int, help="Seed for randomness",
                        default=SEED)
    parser.add_argument("--n_trials", type=int, help="Number of trials",
                        default=N_TRIALS)
    parser.add_argument("--k_list", type=int, help="List of K factor for data stream counting", nargs="+",
                        default=K_LIST)
    args = parser.parse_args()

    random.seed(args.seed)
    execute(args.dir_texts, args.dir_solutions, args.dir_exec_time, args.n_trials, args.k_list)
