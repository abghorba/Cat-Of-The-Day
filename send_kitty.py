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
        None
        
        """
        message = self.twilio_client.messages.create(
            from_ = TWILIO_PHONE_NUMBER,
            to = receving_number,
            body = text_message,
            media_url = [image_url]
        )
        print(f"Message has been {message.status} with SID {message.sid}")
        log_data(f"Message has been {message.status} with SID {message.sid}")


class CatAPIHandler():
    """Class to handle TheCatAPI services."""

    def get_cat_image(self):
        """Sends a request to TheCatAPI and retrieves only an
        image url.

        Parameters
        ----------
        None

        Returns
        -------
        list
            A list containing the image url and text message.
        
        """
        response = requests.get(
            url = CAT_API_URL + '/images/search',
            headers = CAT_API_HEADER
        )

        data = response.json()
        image_url = data[0]['url']

        # Log data
        log_data(data)

        return [image_url, "Here is a random kitty!"]
    
    def get_cat_image_with_fact(self):
        """Sends a request to TheCatAPI to retrieve an image
        along with facts.

        Parameters
        ----------
        None

        Returns
        -------
        list
            A list containing the image url and text message.
        
        """
        response = requests.get(
            url = CAT_API_URL + '/images/search?has_breeds=1?category_ids=4',
            headers = CAT_API_HEADER
        )

        data = response.json()
        image_url = data[0]['url']
        breed_info = data[0]['breeds']
        breed_description = breed_info[0]['description']

        # Log data
        log_data(data)

        return [image_url, breed_description]


def main():
    """Test the script."""

    with open('log.txt', 'w') as f:
        pass

    twilio_message_handler = TwilioMessageHandler()
    cat_api_handler = CatAPIHandler()

    for i in range(10):
        if i % 2 == 0:
            kitty_image_url, kitty_fact = cat_api_handler.get_cat_image_with_fact()
        else:
            kitty_image_url, kitty_fact = cat_api_handler.get_cat_image()

        twilio_message_handler.send_message(
            receving_number = MY_NUMBER,
            text_message = kitty_fact,
            image_url = kitty_image_url
        )

if __name__ == "__main__":
    main()