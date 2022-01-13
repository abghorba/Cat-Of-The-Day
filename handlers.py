import requests
import time

from config import CAT_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
from twilio.rest import Client


CAT_API_URL = 'https://api.thecatapi.com/v1'
CAT_API_HEADER = {'x-api-key': CAT_API_KEY}


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
    with open('log.txt', 'a') as f:
        f.write(data)


class TwilioMessageHandler():
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
            from_ = TWILIO_PHONE_NUMBER,
            to = receiving_number,
            body = text_message,
            media_url = [image_url]
        )

        # Log data
        data = (f'Message Details:\n'
                f'  Receiving Number: {receiving_number}\n'
                f'  Outgoing Message: {text_message}\n'
                f'  Image URL: {image_url}\n'
                f'  Message SID: {message.sid}\n'
                f'  Message Status: {message.status}\n'
                '\n')
        log_data(data)

        print(f"Message has been {message.status} with SID {message.sid}")

        return message.sid


class CatAPIHandler():
    """Class to handle TheCatAPI services."""

    def __init__(self):
        self.CATEGORY_IDS = {
            "boxes": 5,
            "clothes": 15,
            "hats": 1,
            "sinks": 14,
            "space": 2,
            "sunglasses": 4,
            "ties": 7
        }

    def get_cat_image(self, category=None, get_fact=False):
        """Sends a request to TheCatAPI and retrieves only an
        image url.

        Parameters
        ----------
        category : str (optional)
            Optional parameter to get an image of a cat with a
            particular category. Valid categories include
            boxes, clothes, hats, sinks, space, sunglasses, and
            ties.
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
            query = '/images/search?has_breeds=1'
        elif category in self.CATEGORY_IDS:
            query = f'/images/search?category_ids={self.CATEGORY_IDS[category]}'
            message = f"Here is a kitty with {category}!"
        else:
            query = '/images/search'
            message = "Here is a random kitty!"

        # Make request to API and get relevant data
        response = requests.get(
            url = CAT_API_URL + query,
            headers = CAT_API_HEADER
        )
        json_data = response.json()
        image_url = json_data[0]['url']

        # Must collect additional data if we want a fact
        if get_fact:
            try:
                breed_info = json_data[0]['breeds']
                message = breed_info[0]['description']
            except IndexError as e: #There's a bug in the API service
                print("Exception! " + str(e))
                message = "Here is a random kitty!"
                log_data(str(e))

        # Log data
        data = (f'The Cat API Parameters:\n'
                f'  Category: {category}\n'
                f'  Get Fact?: {get_fact}\n'
                f'  API Query: {query}\n')
        log_data(data)

        return [image_url, message]