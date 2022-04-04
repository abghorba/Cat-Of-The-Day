import random
import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# Want to use Natural Language Processing to understand user requests
class TextProcessor():
    """Class to handle text processing."""

    def clean_text(self, text):
        """
        Clean the text to be usable. Strips leading/trailing
        whitespace, strips punctuation, and converts string to
        lowercase.

        :param text: The text to be cleaned
        :return: Cleaned text as a string
        """
        if not text:
            return None

        clean_text = text.strip()
        clean_text = re.sub(r"[^\w\s]", "", clean_text)
        clean_text = clean_text.lower()

        return clean_text

    def find_keywords_in_text(self, keywords, text):
        """
        Given a dictionary of keywords, finds if any keyword
        exists in a text.

        :param keywords: Dictionary containing the keywords to search for
        :param text: The text to search for keywords in
        :return: The first keyword found in text
        """

        # If text has multiple keywords, find the first keyword randomly
        keywords_list = list(keywords.keys())
        random.shuffle(keywords_list)

        for key in keywords_list:

            if key in text:

                return key

        return None

    def preprocess_text(self, text):
        """
        Preprocesses text by stripping whitespace, removing
        punctuation, changing all characters to lowercase,
        tokenizing by whitespaces, and lemmatizing each word.

        :param text: The text to be processed.
        :return: A list of all preprocessed words
        """

        text = text.strip()
        text = re.sub(r"[^\w\s]", "", text)
        text = text.lower()
        text_tokens = text.split(" ")

        stop_words = set(stopwords.words("english"))
        lemmatizer = WordNetLemmatizer()
        processed_text = []

        for word in text_tokens:

            if word not in stop_words:

                lemma = lemmatizer.lemmatize(word)
                processed_text.append(lemma)

        return processed_text
