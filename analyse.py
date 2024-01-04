import argparse
import json
import os

from utils.constants.labels import EXACT_CNT, APPROX_CNT, DS_CNT, FREQ, EXEC_TIME
from utils.constants.parameters import DIR_SOL, DIR_ANALYSIS, K_LIST
from utils.helpers import analyse


def execute(dir_solutions, dir_analysis, k_list):
    if not os.path.exists(dir_solutions):
        raise ValueError(f"Illegal Argument! {dir_solutions} does not exist!")

    if not os.path.exists(dir_analysis):
        raise ValueError(f"Illegal Argument! {dir_analysis} does not exist!")

    for file in [f for f in os.listdir(dir_solutions) if f.endswith('.json')]:
        title = file.split(".")[0]

        with open(os.path.join(dir_solutions, file), "r", encoding="utf8") as fp_input:
            solutions = json.load(fp_input)

        exact_counter_solution = solutions[EXACT_CNT]
        exact_counter_solution[FREQ] = {i[0]: i[1] for i in exact_counter_solution[FREQ]}

        approx_counter_solution = [{char: count for char, count in trial} for trial in solutions[APPROX_CNT][FREQ]]

        data_stream_counter_solution = solutions[DS_CNT]
        for k, v in data_stream_counter_solution.items():
            data_stream_counter_solution[k] = {FREQ: {i[0]: i[1] for i in v[FREQ]}, EXEC_TIME: v[EXEC_TIME]}

        statistics = dict()
        statistics[EXEC_TIME] = {EXACT_CNT: exact_counter_solution[EXEC_TIME],
                                 APPROX_CNT: approx_counter_solution[EXEC_TIME],
                                 DS_CNT: {k: data_stream_counter_solution[k][EXEC_TIME]
                                          for k in data_stream_counter_solution}}
        statistics["Counter"] = analyse(exact_counter_solution,
                                        approx_counter_solution,
                                        data_stream_counter_solution, k_list)


        with open(os.path.join(dir_analysis, f"{title}.json"), "w") as fp:
            json.dump(statistics, fp, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Counter Algorithm Analysis")
    parser.add_argument("--dir_solutions", type=str, help="Directory with the solutions",
                        default=DIR_SOL)
    parser.add_argument("--dir_analysis", type=str, help="Directory to store analysis files",
                        default=DIR_ANALYSIS)
    parser.add_argument("--k_list", type=int, help="List of K factor for data stream counting", nargs="+",
                        default=K_LIST)
    args = parser.parse_args()

    execute(args.dir_solutions, args.dir_analysis, args.k_list)
