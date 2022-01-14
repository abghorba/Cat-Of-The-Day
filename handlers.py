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


class TextProcessor:
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
        query = "/categories"

        response = requests.get(url=CAT_API_URL + query, headers=CAT_API_HEADER)
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
        query = "/breeds"

        response = requests.get(url=CAT_API_URL + query, headers=CAT_API_HEADER)
        # list of each breed
        json_data = response.json()

        for breed_info in json_data:
            breed_name = breed_info["name"].lower()
            breed_id = breed_info["id"]
            breed_ids[breed_name] = breed_id

        return breed_ids

    def get_cat_image(self, category=None, breed=None, get_fact=False):
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
        get_fact : bool (optional)
            Optional parameter to get an image of a cat along
            with a fact. This parameter overrides the category
            parameter, otherwise there will be an empty response.

        Returns
        -------
        list
            A list containing the image url and text message.

        """
        # Configure query and message
        # If we want a fact, we cannot combine queries even if category is specified
        if get_fact:
            query = "/images/search?has_breeds=1"
        elif category in self.CATEGORY_IDS:
            query = f"/images/search?category_ids={self.CATEGORY_IDS[category]}"
            if category in {"hat", "tie"}:
                message = f"Here is a cat wearing a {category}!"
            elif category in {"box", "sink"}:
                message = f"Here is a cat in a {category}!"
            elif category == "clothes":
                message = f"Here is a cat wearing clothes!"
            else:
                message = f"Here is a cat wearing sunglasses!"
        elif breed in self.BREED_IDS:
            query = f"/images/search?breed_ids={self.BREED_IDS[breed]}"
            message = f"Here is a {breed.title()} cat!"
        else:
            query = "/images/search"
            message = "Here is a random cat!"

        # Make request to API and get relevant data
        response = requests.get(url=CAT_API_URL + query, headers=CAT_API_HEADER)
        json_data = response.json()
        image_url = json_data[0]["url"]

        # Must collect additional data if we want a fact
        if get_fact:
            try:
                breed_info = json_data[0]["breeds"]
                message = breed_info[0]["description"]
            except IndexError as e:  # There's a bug in the API service
                print("Exception! " + str(e))
                message = "Here is a random cat!"
                log_data(str(e))

        # Log data
        data = (
            f"The Cat API Parameters:\n"
            f"  Category: {category}\n"
            f"  Get Fact?: {get_fact}\n"
            f"  API Query: {query}\n"
            f"  Response Code: {response.status_code}\n"
        )
        log_data(data)

        return [image_url, message]
