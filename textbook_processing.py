import argparse
import json
import os

from utils.constants.parameters import DIR_ORIGINAL, DIR_PROCESSED, FILE_PROC_STATS
from utils.constants.stopwords import EN_STOPWORDS, FR_STOPWORDS, DE_STOPWORDS, NL_STOPWORDS, FI_STOPWORDS

from utils.helpers import get_language, process_text


def execute(dir_input, dir_output, fp_stats):
    if not os.path.exists(dir_output):
        os.mkdir(dir_output)

    if not fp_stats.endswith(".json"):
        raise Exception("Illegal argument! fp_stats must be a json file!")

    statistics = dict()

    book_titles = [title for title in os.listdir(dir_input) if title.endswith('.txt')]

    for book_title in book_titles:
        title = book_title.split(".")[0]
        # language = get_language(os.path.join(dir_input, book_title))
        language = title

        if language == "english":
            stopwords = EN_STOPWORDS
        elif language == "french":
            stopwords = FR_STOPWORDS
        elif language == "german":
            stopwords = DE_STOPWORDS
        elif language == "dutch":
            stopwords = NL_STOPWORDS
        elif language == "finnish":
            stopwords = FI_STOPWORDS
        else:
            raise Exception(f"Not valid book! System is not prepared to receive a book in {language}.")

        with open(os.path.join(dir_input, book_title), "r", encoding="utf8") as fp_input:
            text = fp_input.read()

            # initial length
            initial_size = len(text)

            # process text
            text = process_text(stream=text, stopwords=stopwords)

            final_size = len(text)

            variation_rate = round((final_size / initial_size) * 100, 2)
            statistics[title] = {"initial_size": initial_size, "final_size": final_size,
                                 "variation_rate": variation_rate}

            with open(os.path.join(dir_output, book_title), "w", encoding="utf8") as fp:
                fp.write(text)

    with open(fp_stats, "w") as fp:
        json.dump(statistics, fp, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Text conversion")
    parser.add_argument("--dir_input", type=str, help="Directory with original textbooks",
                        default=DIR_ORIGINAL)
    parser.add_argument("--dir_output", type=str, help="Directory to store converted textbooks",
                        default=DIR_PROCESSED)
    parser.add_argument("--fp_stats", type=str, help="Filename to store processing results",
                        default=FILE_PROC_STATS)
    args = parser.parse_args()

    execute(args.dir_input, args.dir_output, args.fp_stats)
