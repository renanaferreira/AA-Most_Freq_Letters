import argparse
import json
import os
import random
import time

from utils.constants.labels import EXACT_CNT, APPROX_CNT, DS_CNT, EXEC_TIME, FREQ
from utils.constants.parameters import DIR_PROCESSED, SEED, N_TRIALS, K_LIST, DIR_SOL, FILE_TIME_STATS
from utils.helpers import exact_counter, experiment_approximate_counter, experiment_data_stream_counter, get_mean


def execute(dir_texts, dir_solutions, file_time_stats, n_trials, k_list):
    if not os.path.exists(dir_texts):
        raise ValueError(f"Illegal Argument! {dir_texts} does not exist!")

    if not os.path.exists(dir_solutions):
        raise ValueError(f"Illegal Argument! {dir_solutions} does not exist!")

    exec_time_stats = dict()
    for book_title in [title for title in os.listdir(dir_texts) if title.endswith('.txt')]:
        with open(os.path.join(dir_texts, book_title), "r", encoding="utf8") as fp:
            text = fp.read()

        # Exact counter
        exact_count = exact_counter(text).to_json()
        # Data Stream counter
        ds_count = experiment_data_stream_counter(text, k_list)
        # Approximate counter
        start = time.time()
        approx_count = experiment_approximate_counter(text, n_trials)
        duration = time.time() - start
        print(f"{book_title} - Approximate count duration: {duration}s")

        title = book_title.split(".")[0]

        ds_time = {k: round(ds_count[k][EXEC_TIME], 4) for k in ds_count}
        ds_time["avg"] = round(get_mean([ds_count[k][EXEC_TIME] for k in ds_count]), 4)

        # Store execution time
        exec_time_stats[title] = {EXACT_CNT: round(exact_count[EXEC_TIME], 4),
                                  APPROX_CNT: round(approx_count[EXEC_TIME], 4),
                                  DS_CNT: ds_time}

        # Store solutions
        solutions = {EXACT_CNT: exact_count[FREQ],
                     APPROX_CNT: approx_count[FREQ],
                     DS_CNT: {k: ds_count[k][FREQ] for k in ds_count}}
        with open(os.path.join(dir_solutions, f"{title}.json"), "w", encoding="utf8") as fp:
            json.dump(solutions, fp, ensure_ascii=False)

    with open(file_time_stats, "w") as fp:
        json.dump(exec_time_stats, fp, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Most Frequent Letters Count")
    parser.add_argument("--dir_texts", type=str, help="Directory with texts to count",
                        default=DIR_PROCESSED)
    parser.add_argument("--dir_solutions", type=str, help="Directory to store count solutions",
                        default=DIR_SOL)
    parser.add_argument("--file_time_stats", type=str, help="File to store execution time statistics",
                        default=FILE_TIME_STATS)
    parser.add_argument("--seed", type=int, help="Seed for randomness",
                        default=SEED)
    parser.add_argument("--n_trials", type=int, help="Number of trials",
                        default=N_TRIALS)
    parser.add_argument("--k_list", type=int, help="List of K factor for data stream counting", nargs="+",
                        default=K_LIST)
    args = parser.parse_args()

    random.seed(args.seed)
    execute(args.dir_texts, args.dir_solutions, args.file_time_stats, args.n_trials, args.k_list)
