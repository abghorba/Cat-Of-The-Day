import json
import logging as log
import os
from datetime import datetime

from flask import Flask, request

from src.request_processor import RequestProcessor
from src.the_cat_api_handler import CatAPIHandler
from src.twilio_messaging import TwilioMessageHandler

ERROR_MESSAGE = "Sorry, I didn't understand your request."
CHARACTER_LIMIT_REACHED_MESSAGE = "Please limit your request to less than 100 characters."

app = Flask(__name__)
twilio = TwilioMessageHandler()
cat_api = CatAPIHandler()
request_processor = RequestProcessor()

# Set up logger
log_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "-log.txt"
log_directory = f"{os.getcwd()}/logs"
logfile = os.path.abspath(f"{log_directory}/{log_filename}")

# Make the log directory if necessary
if not os.path.exists(log_directory):
    os.mkdir(log_directory)

log_format = "%(asctime)s\t%(module)20s:%(lineno)4d\t: %(message)s"
log.basicConfig(filename=logfile, format=log_format, level=log.INFO)
log.getLogger().addHandler(log.StreamHandler())


@app.route("/sms", methods=["POST"])
def sms_reply():
    """Respond to incoming messages."""

    incoming_message = request.values.get("Body", None)
    incoming_number = request.values.get("From", None)

    log.info(f"Message received: {incoming_message}")

    cat_image_url = None
    message = ERROR_MESSAGE

    if len(incoming_message) > 100:
        message = CHARACTER_LIMIT_REACHED_MESSAGE

    else:
        action, obj = request_processor.process_request(user_request=incoming_message)

        if action and obj:
            # Check if any of the categories are in query
            requested_category = request_processor.get_keywords_in_string(cat_api.CATEGORY_IDS, obj)

            # Check if any of the breeds are in query
            requested_breed = request_processor.get_keywords_in_string(cat_api.BREED_IDS, obj)

            # Make the API call
            cat_image_url, message = cat_api.get_cat_image(category=requested_category, breed=requested_breed)

    message_sid = None

    if not app.config["TESTING"]:
        message_sid = twilio.send_message(
            receiving_number=incoming_number,
            text_message=message,
            image_url=cat_image_url,
        )

    # Create response dictionary
    response = {
        "incoming_message": incoming_message,
        "receiving_number": incoming_number,
        "outgoing_message": message,
        "image_url": cat_image_url,
        "status": message_sid,
    }
    return json.dumps(response)


if __name__ == "__main__":
    app.run()
