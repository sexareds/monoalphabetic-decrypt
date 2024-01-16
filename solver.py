import re

LETTER_FREQUENCY = {
    "e": 12.7, "t": 9.06, "a": 8.17, "o": 7.51, "i": 6.97, "n": 6.75, "s": 6.33, "h": 6.09,
    "r": 5.99, "d": 4.25, "l": 4.03, "c": 2.78, "u": 2.76, "m": 2.41, "w": 2.36, "f": 2.23,
    "g": 2.02, "y": 1.97, "p": 1.93, "b": 1.29, "v": 0.98, "k": 0.77, "j": 0.15, "x": 0.15,
    "q": 0.10, "z": 0.07
}

BIGRAMS_FREQUENCY = {
    "th": 3.56, "he": 3.07, "in": 2.43, "er": 2.05, "an": 1.99, "re": 1.85, "on": 1.76, "at": 1.49, "en": 1.45, "nd": 1.35, "ti": 1.34, "es": 1.34, "or": 1.28, "te": 1.20,
    "of": 1.17, "ed": 1.17, "is": 1.13, "it": 1.12, "al": 1.09, "ar": 1.07, "st": 1.05, "to": 1.05, "nt": 1.04, "ng": 0.95, "se": 0.93, "ha": 0.93, "as": 0.87, "ou": 0.87,
    "io": 0.83, "le": 0.83, "ve": 0.83, "co": 0.79, "me": 0.79, "de": 0.76, "hi": 0.76, "ri": 0.73, "ro": 0.73, "ic": 0.70, "ne": 0.69, "ea": 0.69, "ra": 0.69, "ce": 0.65
}

TRIGRAMS_FREQUENCY = {
    "the": 3.51, "and": 1.59, "ing": 1.15, "her": 0.82, "hat": 0.65, "his": 0.60, "tha": 0.59, "ere": 0.56, "for": 0.55, "ent": 0.53,
    "ion": 0.51, "ter": 0.46, "was": 0.46, "you": 0.44, "ith": 0.43, "ver": 0.43, "all": 0.42, "wit": 0.40, "thi": 0.39, "tio": 0.38,
}

def calculate_letter_frequencies(text):
    frequencies = {}
    letters_count = 0

    # we are calculating the number of occurrence for each letter.
    for letter in text:
        if letter.isalpha():
            if frequencies.get(letter, None):
                frequencies[letter] += 1
            else:
                frequencies[letter] = 1
            letters_count += 1

    for letter, count in frequencies.items():
        frequencies[letter] = count / letters_count

    return dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))


def calculate_n_gram_frequencies(cipher_text: str, n_gram_length: int = 2):

    n_gram_frequencies = {}
    n_grams_count = 0

    for i in range(len(cipher_text) - n_gram_length - 1):
        n_gram = cipher_text[i:i + n_gram_length]
        if n_gram.isalpha() and len(n_gram) == n_gram_length:
            if n_gram in n_gram_frequencies:
                n_gram_frequencies[n_gram] += 1
            else:
                n_gram_frequencies[n_gram] = 1
            n_grams_count += 1

    for letter, count in n_gram_frequencies.items():
        n_gram_frequencies[letter] = count / n_grams_count

    # Sort the dictionary
    n_gram_frequencies = dict(sorted(n_gram_frequencies.items(), key=lambda item: item[1], reverse=True))
    top_10 = dict(list(n_gram_frequencies.items())[:10])
    return top_10


def calculate_doubles_frequencies(cipher_text: str):

   #Finding all the double letter combinations.

    doubles_frequencies = {}
    doubles_count = 0

    for i in range(len(cipher_text) - 1):
        double = cipher_text[i:i + 2]
        if double.isalpha() and double[0] == double[1]:
            if double in doubles_frequencies:
                doubles_frequencies[double] += 1
            else:
                doubles_frequencies[double] = 1
            doubles_count += 1

    for double, count in doubles_frequencies.items():
        doubles_frequencies[double] = count / doubles_count

    return dict(sorted(doubles_frequencies.items(), key=lambda item: item[1], reverse=True))


def replace_most_common(text, frequencies):
    sorted_frequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
    replacement_dict = dict(zip([item[0] for item in sorted_frequencies], LETTER_FREQUENCY.keys()))

    pattern = re.compile('|'.join(re.escape(key) for key in replacement_dict.keys()))

    return pattern.sub(lambda x: replacement_dict[x.group()], text)

def main():
    #main function
    class Theme:
        GREEN = "\033[92m"
        DARKCYAN = "\033[36m"
        BOLD = "\033[1m"
        END = "\033[0m"
    print("********************************************************************************\n")
    print(Theme.GREEN+ Theme.BOLD +"            Welcome to the Frequency Analysis program\n" + Theme.END)
    print(Theme.DARKCYAN+"This program lets you obtain the frequency of each letter \n in the  Monoalphabetic cipher text file and prints the \n results in the console.\n"+Theme.END)
    print("********************************************************************************")

    # Reading the cipher text from text file
    with open('cipher_text.txt', 'r', encoding='UTF-8') as file:
        cipher_text = file.read()

    # Performing letter frequency analysis
    letter_frequencies = calculate_letter_frequencies(cipher_text)
    print(Theme.GREEN+"\nLetter frequencies:\n"+Theme.END)
    for letter, frequency in letter_frequencies.items():
        print(f'{letter} = {round(frequency * 100, 2)}%')

    # Performing letter-combination frequency analysis in different combinations
    two_letters_combinations_frequencies = calculate_n_gram_frequencies(cipher_text, n_gram_length=2)
    three_letters_combinations_frequencies = calculate_n_gram_frequencies(cipher_text, n_gram_length=3)
    double_letters_combinations_frequencies = calculate_doubles_frequencies(cipher_text)
    four_letters_combinations_frequencies = calculate_n_gram_frequencies(cipher_text, n_gram_length=4)

    print(Theme.GREEN+"\nTwo letters combinations frequencies:\n"+Theme.END)
    for letter, frequency in two_letters_combinations_frequencies.items():
        print(f'{letter} = {round(frequency * 100, 2)}%')

    print(Theme.GREEN+"\n Three letters combinations frequencies:\n"+Theme.END)
    for letter, frequency in three_letters_combinations_frequencies.items():
        print(f'{letter} = {round(frequency * 100, 2)}%')

    print(Theme.GREEN+"\nDouble letters combinations frequencies:\n"+Theme.END)
    for double, frequency in double_letters_combinations_frequencies.items():
        print(f'{double} = {round(frequency * 100, 2)}%')

    print(Theme.GREEN+"\nFour letters combinations frequencies:\n"+Theme.END)
    for letter, frequency in four_letters_combinations_frequencies.items():
        print(f'{letter} = {round(frequency * 100, 2)}%')

    # Replacing the most common letter with the most common letter in English
    print(Theme.GREEN+"\nReplacing the most common letter with the most common letter in English:\n"+Theme.END)
    # Replace most common letter
    cipher_text_replaced_letter = replace_most_common(cipher_text, letter_frequencies)
    print(Theme.GREEN + "\nCipher text with most common letter replaced:\n" + Theme.END)
    print(cipher_text_replaced_letter)

    # # Replace most common bigram
    # cipher_text_replaced_bigram = replace_most_common(cipher_text, two_letters_combinations_frequencies)
    # print(Theme.GREEN + "\nCipher text with most common bigram replaced:\n" + Theme.END)
    # print(cipher_text_replaced_bigram)

    # # Replace most common trigram
    # cipher_text_replaced_trigram = replace_most_common(cipher_text, three_letters_combinations_frequencies)
    # print(Theme.GREEN + "\nCipher text with most common trigram replaced:\n" + Theme.END)
    # print(cipher_text_replaced_trigram)

if __name__ == '__main__':
    main()
