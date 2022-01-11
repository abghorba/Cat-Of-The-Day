import requests
import time
import json

from config import CAT_API_KEY, MY_NUMBER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
from twilio.rest import Client


CAT_API_URL = 'https://api.thecatapi.com/v1'
CAT_API_HEADER = {'x-api-key': CAT_API_KEY}


def log_data(json_data):
    """Logs the json response from each request to TheCatAPI
    and the Twilio message status/SID.
    
    Parameters
    ----------
    json_data : JSON
        Data to be logged in a JSON object.

    Returns
    -------
    None

    """
    with open('log.txt', 'a') as f:
        json_formatted_str = json.dumps(json_data, indent=2)
        f.write(json_formatted_str)
        f.write('\n')


class TwilioMessageHandler():
    """Class to handle Twilio services."""

    def __init__(self):
        """Initializes the object with the Twilio client."""
        self.twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def send_message(self, receving_number, text_message, image_url=None):
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
        status : str
            A string containing the message status along
            with the security identifier.
        
        """
        message = self.twilio_client.messages.create(
            from_ = TWILIO_PHONE_NUMBER,
            to = receving_number,
            body = text_message,
            media_url = [image_url]
        )
        status = f"Message has been {message.status} with SID {message.sid}"
        print(status)
        log_data(status)
        return status


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
        data = response.json()
        image_url = data[0]['url']

        # Must collect additional data if we want a fact
        if get_fact:
            try:
                breed_info = data[0]['breeds']
                message = breed_info[0]['description']
            except IndexError as e: #There's a bug in the API service
                print("Exception! " + str(e))
                message = "Here is a random kitty!"
                log_data(str(e))

        # Log data
        log_data(f'Category: {category}')
        log_data(f'Get Fact?: {get_fact}')
        log_data(f'Query: {query}')
        log_data(f'Message: {message}')
        log_data(data)

        return [image_url, message]