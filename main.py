import os
import re

ARTICLES_PATH = "data/"
PROCESSED_ARTICLES_PATH = ARTICLES_PATH + "/processed/"


# Process the files.
def process_files():
    for file_name in os.listdir(ARTICLES_PATH):
        if file_name.endswith(".txt"):
            with open(ARTICLES_PATH + file_name) as file:
                contents = file.readlines()
                new_contents = []
                for i, line in enumerate(contents):
                    new_contents.append(line.lower()
                                        .replace(".", "\n")
                                        .replace("?", "\n")
                                        .replace("!", "\n")
                                        .replace(":", "\n")
                                        .replace("'s", " is")
                                        .replace("'t", " not")
                                        .replace("'m", " am")
                                        .replace("'ve", " have")
                                        .replace("'re", " are")
                                        .replace("'ll", " will")
                                        .replace("•", ""))
                with open(PROCESSED_ARTICLES_PATH + "processed-" + file_name, "w") as new_file:
                    new_file.write("".join(new_contents))


def calculate_meta_features():
    for file_name in os.listdir(PROCESSED_ARTICLES_PATH):
        if file_name.endswith(".txt"):
            with open(PROCESSED_ARTICLES_PATH + file_name) as file:
                contents = file.readlines()
                contents = [s for s in contents if not s == "\n"]
                num_words = len("".join(contents).split())
                num_sentences = calculate_num_sentences(contents)
                max_words = max_words_per_sentence(contents)
                min_words = min_words_per_sentence(contents)
                avg_sentence_length = average_sentence_length(contents)
                max_syllable = max_syllables(contents)
                min_syllable = min_syllables(contents)
                avg_syllables = average_syllables(contents)
                fres = calculate_fres(contents)

                print(
                    "Num Words: {0}, "
                    "Num Sentences: {1}, "
                    "Max Words: {2}, "
                    "Min Words: {3}, "
                    "Avg. Sentence Length: {4}, "
                    "Max Syllables: {5}, "
                    "Min Syllables: {6}, "
                    "Avg. Syllables: {7}, "
                    "FRES: {8}".format(
                        num_words,
                        num_sentences,
                        max_words,
                        min_words,
                        "{:.2f}".format(avg_sentence_length),
                        max_syllable,
                        min_syllable,
                        "{:.2f}".format(avg_syllables),
                        "{:.2f}".format(fres))
                )


def calculate_num_sentences(contents):
    return len(contents)


def max_words_per_sentence(contents):
    max_words = 0
    for line in contents:
        if len(line.split()) > max_words:
            max_words = len(line.split())
    return max_words


def min_words_per_sentence(contents):
    min_words = 999
    for line in contents:
        if len(line.split()) != 0 and len(line.split()) < min_words:
            min_words = len(line.split())
    return min_words


def average_sentence_length(contents):
    num_sentences = len(contents)
    num_words = len("".join(contents).split())
    return num_words / num_sentences


def max_syllables(contents):
    max_syllable = 0
    for word in "".join(contents).split():
        count = find_syllables(word)
        if count > max_syllable:
            max_syllable = count
    return max_syllable


def min_syllables(contents):
    min_syllable = 999
    for word in "".join(contents).split():
        count = find_syllables(word)
        if count < min_syllable and count != 0:
            min_syllable = count
    return min_syllable


def average_syllables(contents):
    num_words = len("".join(contents).split())
    total_syllables = 0
    for word in "".join(contents).split():
        total_syllables += find_syllables(word)
    return total_syllables / num_words


def find_syllables(word):
    syllables = 0
    discarded = 0

    # If letters < 3
    if len(word) <= 3:
        syllables = 1
        return syllables

    # Discard trailing e
    if word[-1:] == "e":
        if word[-2:] == "le":
            pass

        else:
            discarded += 1

    # Consecutive Vowels
    discarded += len(re.findall(r'[eaoui][eaoui]', word))

    # Count vowels in word
    vowels = len(re.findall(r'[eaoui]', word))

    # Deal with scenarios involving y
    if word[-1:] == "y" and word[-2] not in "aeoui":
        syllables += 1
    for i, j in enumerate(word):
        if j == "y":
            if (i != 0) and (i != len(word) - 1):
                if word[i - 1] not in "aeoui" and word[i + 1] not in "aeoui":
                    syllables += 1

    return vowels - discarded + syllables


def calculate_fres(contents):
    total_syllables = 0
    for word in "".join(contents).split():
        total_syllables += find_syllables(word)
    sentence_difficulty = len("".join(contents).split()) / calculate_num_sentences(contents)
    word_difficulty = total_syllables / len("".join(contents).split())

    return 206.835 - 1.015 * sentence_difficulty - 84.6 * word_difficulty


if __name__ == "__main__":
    process_files()
    calculate_meta_features()
