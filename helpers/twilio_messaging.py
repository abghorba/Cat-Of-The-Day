import logging

from helpers.configs import TWILIO_ACCOUNT_SID
from helpers.configs import TWILIO_AUTH_TOKEN
from helpers.configs import TWILIO_PHONE_NUMBER
from twilio.rest import Client


class TwilioMessageHandler():
    """Class to handle Twilio services."""

    def __init__(self):
        """Initializes the object with the Twilio client."""

        self.twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def send_message(self, receiving_number, text_message, image_url=None):
        """
        Uses Twilio to send a message to a specified number.

        :param receiving_number: Number that will be receiving the message
        :param text_message: Body of the text that will be sent
        :param image_url: String url of the image that will be sent
        :return: String containing the message security identifier
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
            f"    Receiving Number: {receiving_number}\n"
            f"    Outgoing Message: {text_message}\n"
            f"    Image URL: {image_url}\n"
            f"    Message SID: {message.sid}\n"
            f"    Message Status: {message.status}\n"
            "\n"
        )
        logging.info(data)

        logging.info(f"Message has been {message.status} with SID {message.sid}")

        return message.sid
