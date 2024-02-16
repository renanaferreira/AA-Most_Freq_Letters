import argparse
import os

from utils.constants.parameters import DIR_ORIGINAL, DIR_FREQS
from utils.helpers import get_language, get_words_frequency


def execute(dir_input, dir_output):
    if not os.path.exists(dir_input):
        raise ValueError(f"Illegal Argument! {dir_input} does not exist!")
    if not os.path.exists(dir_output):
        raise ValueError(f"Illegal Argument! {dir_output} does not exist!")

    for book_title in [title for title in os.listdir(dir_input) if title.endswith('.txt')]:
        title = book_title.split(".")[0]

        with open(os.path.join(dir_input, book_title), "r", encoding="utf8") as fp_input:
            text = fp_input.read()

        counter = get_words_frequency(text)

        with open(os.path.join(dir_output, f"{title}.txt"), "w") as output_fp:
            for item in counter:
                output_fp.write(f"{item[0]}: {item[1]}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count words frequency")
    parser.add_argument("--dir_input", type=str, help="Directory with textbooks",
                        default=DIR_ORIGINAL)
    parser.add_argument("--dir_output", type=str, help="Directory to store outputs",
                        default=DIR_FREQS)
    args = parser.parse_args()

    execute(args.dir_input, args.dir_output)
