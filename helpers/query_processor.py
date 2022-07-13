import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


STOP_WORDS = set(stopwords.words('english'))

# Want to use Natural Language Processing to understand user requests
class QueryProcessor():
    """Class to handle query processing."""

    def _clean_text(self, text):
        """
        Clean the text to be usable. Strips leading/trailing
        whitespace, strips punctuation, and converts string to
        lowercase.

        :param text: The text to be cleaned
        :return: Cleaned text as a string
        """
        if not text:
            return ""

        clean_text = text.strip()
        clean_text = re.sub(r"[^\w\s\']", "", clean_text)g
        clean_text = clean_text.lower()

        return clean_text

    def _preprocess_text(self, text):
        """
        Preprocesses text by stripping whitespace, removing
        punctuation, changing all characters to lowercase,
        tokenizing by whitespaces, and lemmatizing each word.

        :param text: The text to be processed.
        :return: A list of all preprocessed words
        """

        cleaned_text = self._clean_text(text)
        text_tokens = word_tokenize(cleaned_text)

        lemmatizer = WordNetLemmatizer()
        processed_text = []

        for word in text_tokens:

            if word not in STOP_WORDS:
                lemma = lemmatizer.lemmatize(word)
                processed_text.append(lemma)

        return processed_text

    def find_keywords_in_text(self, keywords, text):
        """
        Given a set of keywords, returns a dictionary with
        the found keywords and the frequency of the keyword in
        text.

        :param keywords: Set containing the keywords to search for
        :param text: The text to search for keywords in
        :return: The first keyword found in text
        """

        if not keywords or not isinstance(keywords, set):
            raise TypeError("keywords param must be a set")

        if not text or not isinstance(text, str):
            raise TypeError("text param must be a str")

        preprocessed_text = self._preprocess_text(text)
        found_keywords = {}

        for word in preprocessed_text:

            if word in keywords:
                found_keywords[word] =  found_keywords.get(word, 0) + 1

        return found_keywords

    def find_key_phrases_in_text(self, key_phrases, text):
        """
        Given a set of key phrases, returns a dictionary with
        the found key phrases and the frequency of the key phrase in
        text.

        A key phrase is defined as any string.

        :param key_phrases: Set containing the key_phrases to search for
        :param text: The text to search for keywords in
        :return: The first keyword found in text
        """

        if not key_phrases or not isinstance(key_phrases, set):
            raise TypeError("keywords param must be a set")

        if not text or not isinstance(text, str):
            raise TypeError("text param must be a str")

        preprocessed_text = " ".join(self._preprocess_text(text))
        print(preprocessed_text)

        found_key_phrases = {}

        for key_phrase in key_phrases:

            if key_phrase in preprocessed_text:
                found_key_phrases[key_phrase] = preprocessed_text.count(key_phrase)

        return found_key_phrases

