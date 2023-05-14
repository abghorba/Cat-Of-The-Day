import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CAT_API_KEY = os.getenv("CAT_API_KEY")
MY_NUMBER = os.getenv("MY_NUMBER")


class TwilioCredentials:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.phone_number = os.getenv("TWILIO_PHONE_NUMBER")

    @property
    def empty_credentials(self):
        """Returns True if any credential is empty; False otherwise"""

        return not (bool(self.account_sid) and bool(self.auth_token) and bool(self.phone_number))
