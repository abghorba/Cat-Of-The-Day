import random
import re
import requests

from config import (
    CAT_API_KEY,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
)
from twilio.rest import Client

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


CAT_API_URL = "https://api.thecatapi.com/v1"
CAT_API_HEADER = {"x-api-key": CAT_API_KEY}


def log_data(data):
    """Logs data from specified areas in the API handler classes.

    Parameters
    ----------
    data : str
        Data to be logged.

    Returns
    -------
    None

    """
    with open("log.txt", "a") as f:
        f.write(data)


# Want to use Natural Language Processing to understand user requests
class TextProcessor:
    """Class to handle text processing."""

    def clean_text(self, text):
        """Clean the text to be usable. Strips leading/trailing
        whitespace, strips punctuation, and converts string to
        lowercase.

        Parameters
        ----------
        text : str
            The text to be cleaned.

        Returns
        -------
        clean_text : str
            The text that has been cleaned.

        """
        clean_text = text.strip()
        clean_text = re.sub(r"[^\w\s]", "", clean_text)
        clean_text = clean_text.lower()
        return clean_text

    def find_keywords_in_text(self, keywords, text):
        """Given a dictionary of keywords, finds if any keyword
        exists in a text.

        Parameters
        ----------
        keywords : dict
            A dictionary containing the keywords to search for.
        text : str
            The text to search for keywords in.

        Returns
        -------
        key : str or None
            The first keyword that is found in text.

        """
        # If text has multiple keywords, find the first keyword randomly
        keywords_list = list(keywords.keys())
        random.shuffle(keywords_list)

        for key in keywords_list:
            if key in text:
                return key

        return None

    def preprocess_text(self, text):
        """Preprocesses text by stripping whitespace, removing
        punctuation, changing all characters to lowercase,
        tokenizing by whitespaces, and lemmatizing each word.

        Parameters
        ----------
        text : str
            The text to be processed.

        Returns
        -------
        processed_text : list
            A list of all preprocessed words.

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


class TwilioMessageHandler:
    """Class to handle Twilio services."""

    def __init__(self):
        """Initializes the object with the Twilio client."""
        self.twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def send_message(self, receiving_number, text_message, image_url=None):
        """Uses Twilio to send a message to a specified number.

        Parameters
        ----------
        receiving_number : str
            The number that is receiving the message.
        text_message : str
            The body of the text that will be sent.
        image_url : str
            The url of the image to be sent.

        Returns
        -------
        str
            A string containing the message security identifier.

        """
        message = self.twilio_client.messages.create(
            from_=TWILIO_PHONE_NUMBER,
            to=receiving_number,
            body=text_message,
            media_url=[image_url],
        )

        # Log data
        data = (
            f"Message Details:\n"
            f"  Receiving Number: {receiving_number}\n"
            f"  Outgoing Message: {text_message}\n"
            f"  Image URL: {image_url}\n"
            f"  Message SID: {message.sid}\n"
            f"  Message Status: {message.status}\n"
            "\n"
        )
        log_data(data)

        print(f"Message has been {message.status} with SID {message.sid}")

        return message.sid


class CatAPIHandler:
    """Class to handle TheCatAPI services."""

    def __init__(self):
        self.CATEGORY_IDS = self._get_category_ids()
        self.BREED_IDS = self._get_breed_ids()

    def _get_category_ids(self):
        """Sends a request to The Cat API to retrieve all
        category ids and compile into a dictionary.

        Parameters
        ----------
        None

        Returns
        -------
        category_ids : dict
            Dictionary mapping the category keyword to its
            category id.

        """
        category_ids = {}
        parameter = "/categories"

        response = requests.get(url=CAT_API_URL + parameter, headers=CAT_API_HEADER)
        # list of each category
        json_data = response.json()

        lemmatizer = WordNetLemmatizer()
        for category_info in json_data:
            category_name = lemmatizer.lemmatize(category_info["name"])
            category_id = category_info["id"]
            category_ids[category_name] = category_id

        return category_ids

    def _get_breed_ids(self):
        """Sends a GET request to The Cat API to retrieve all
        breed ids and compile into a dictionary.

        Parameters
        ----------
        None

        Returns
        -------
        breed_ids : dict
            Dictionary mapping the breed name to its
            breed id.

        """
        breed_ids = {}
        parameter = "/breeds"

        response = requests.get(url=CAT_API_URL + parameter, headers=CAT_API_HEADER)
        # list of each breed
        json_data = response.json()

        for breed_info in json_data:
            breed_name = breed_info["name"].lower()
            breed_id = breed_info["id"]
            breed_ids[breed_name] = breed_id

        return breed_ids

    def get_cat_image(self, category=None, breed=None):
        """Sends a request to TheCatAPI and retrieves only an
        image url.

        Parameters
        ----------
        category : str (optional)
            Optional parameter to get an image of a cat with a
            particular category. Valid categories include
            boxes, clothes, hats, sinks, space, sunglasses, and
            ties.
        breed : str (optional)
            Optional parameter to get an image of a cat that is
            a specified breed.

        Returns
        -------
        list
            A list containing the image url and text message.

        """
        # Configure query and message
        # Category will get precedence if both category and breed are specified
        if category in self.CATEGORY_IDS:
            parameter = f"/images/search?category_ids={self.CATEGORY_IDS[category]}"
            if category in {"hat", "tie"}:
                message = f"Here is a cat wearing a {category}!"
            elif category in {"box", "sink"}:
                message = f"Here is a cat in a {category}!"
            elif category == "clothes":
                message = f"Here is a cat wearing clothes!"
            elif category == "space":
                message = f"Here is a cat in space!"
            else:
                message = f"Here is a cat wearing sunglasses!"
        elif breed in self.BREED_IDS:
            parameter = f"/images/search?breed_ids={self.BREED_IDS[breed]}"
            message = f"Here is a {breed.title()} cat!"
        else:
            parameter = "/images/search"
            message = "Here is a random cat!"

        # Make request to API and get relevant data
        response = requests.get(url=CAT_API_URL + parameter, headers=CAT_API_HEADER)
        json_data = response.json()
        image_url = json_data[0]["url"]

        # Log data
        data = (
            f"The Cat API Parameters:\n"
            f"  Category?: {category}\n"
            f"  Breed?: {breed}\n"
            f"  API Parameter: {parameter}\n"
            f"  Response Code: {response.status_code}\n"
        )
        log_data(data)

        return [image_url, message]
