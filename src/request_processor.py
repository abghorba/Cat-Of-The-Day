import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


class RequestProcessor:
    """Class to handle text processing. Uses Natural Language Processing to understand user requests."""

    def __init__(self):
        self.acceptable_verbs = {"show", "get", "see", "send", "view", "give", "receive"}

    def process_request(self, user_request):
        """
        Given a raw user request, use NLTK to identify the action and the object of the request.

        :param user_request: Raw user input (text)
        :return: Tuple of (verb, object)
        """

        # Tokenize the sentence
        tokens = word_tokenize(user_request.lower())

        # Remove stop words and lemmatize the tokens
        stop_words = set(stopwords.words("english"))
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]

        # Find the action and object of the sentence
        action = ""
        obj = ""

        for i in range(len(tokens)):
            if tokens[i] in self.acceptable_verbs:
                action = tokens[i].translate(str.maketrans("", "", string.punctuation)).strip()
                obj = " ".join(tokens[i + 1 :]).translate(str.maketrans("", "", string.punctuation)).strip()
                break

        return action, obj

    @staticmethod
    def get_keywords_in_string(keywords, string_):
        """
        For a given list of keywords, search if any keyword exists in the given string. Return the first keyword
        found in string.

        :param keywords: List of keywords
        :param string_: String to search in
        :return: First keyword found, else None
        """

        for word in keywords:
            if word in string_:
                return word

        return None
