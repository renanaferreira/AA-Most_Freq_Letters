import argparse
import json
import os

from utils.constants.labels import EXACT_CNT, APPROX_CNT, DS_CNT, FREQ, EXEC_TIME
from utils.constants.parameters import DIR_SOL, DIR_ANALYSIS
from utils.helpers import analyse


def execute(dir_solutions, dir_analysis):
    if not os.path.exists(dir_solutions):
        raise ValueError(f"Illegal Argument! {dir_solutions} does not exist!")

    for file in [f for f in os.listdir(dir_solutions) if f.endswith('.json')]:
        title = file.split(".")[0]

        with open(os.path.join(dir_solutions, file), "r", encoding="utf8") as fp_input:
            solutions = json.load(fp_input)

        exact_counter_solution = solutions[EXACT_CNT]
        exact_counter_solution[FREQ] = {i[0]: i[1] for i in exact_counter_solution[FREQ]}

        approx_counter_solution = solutions[APPROX_CNT]
        approx_counter_solution = [{FREQ: {i[0]: i[1] for i in item[FREQ]}, EXEC_TIME: item[EXEC_TIME]}
                                   for item in approx_counter_solution]

        data_stream_counter_solution = solutions[DS_CNT]
        for k, v in data_stream_counter_solution.items():
            data_stream_counter_solution[k] = {FREQ: {i[0]: i[1] for i in v[FREQ]}, EXEC_TIME: v[EXEC_TIME]}

        statistics = analyse(exact_counter_solution, approx_counter_solution, data_stream_counter_solution)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Counter Algorithm Analysis")
    parser.add_argument("--dir_solutions", type=str, help="Directory with the solutions",
                        default=DIR_SOL)
    parser.add_argument("--dir_analysis", type=str, help="Directory to store analysis files",
                        default=DIR_ANALYSIS)
    args = parser.parse_args()

    execute(args.dir_solutions, args.dir_analysis)
