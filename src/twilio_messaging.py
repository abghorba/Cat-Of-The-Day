import logging as log

from twilio.rest import Client

from src.utilities import TwilioCredentials


class TwilioMessageHandler:
    """Class to handle Twilio services."""

    def __init__(self):
        """Initializes the object with the Twilio client."""

        try:
            self.twilio_credentials = TwilioCredentials()
            self.twilio_client = Client(self.twilio_credentials.account_sid, self.twilio_credentials.auth_token)
            self.twilio_client.incoming_phone_numbers.list()
            log.info("Authentication to Twilio successful")
            self.successful_auth = True

        except:
            log.error("Authentication to Twilio unsuccessful")
            self.successful_auth = False

    def send_message(self, receiving_number, text_message, image_url=None):
        """
        Uses Twilio to send a message to a specified number.

        :param receiving_number: Number that will be receiving the message
        :param text_message: Body of the text that will be sent
        :param image_url: String url of the image that will be sent
        :return: String containing the message security identifier
        """

        if not self.successful_auth:
            return

        message = self.twilio_client.messages.create(
            from_=self.twilio_credentials.phone_number,
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
        log.info(data)

        log.info(f"Message has been {message.status} with SID {message.sid}")

        return message.sid
