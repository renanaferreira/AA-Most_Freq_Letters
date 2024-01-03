import string
from collections import Counter


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
