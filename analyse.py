import argparse
import json
import os

from utils.constants.parameters import DIR_SOL


def execute(dir_solutions):
    if not os.path.exists(dir_solutions):
        raise ValueError(f"Illegal Argument! {dir_solutions} does not exist!")

    files = [f for f in os.listdir(dir_solutions) if f.endswith('.json')]

    for file in files:
        title = file.split(".")[0]
        with open(os.path.join(dir_solutions, file), "r", encoding="utf8") as fp_input:
            solutions = json.load(fp_input)

        print(solutions)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Counter Algorithm Analysis")
    parser.add_argument("--dir_solutions", type=str, help="Directory with the solutions",
                        default=DIR_SOL)

    args = parser.parse_args()

    execute(args.dir_solutions)
