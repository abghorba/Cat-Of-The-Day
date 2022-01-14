from flask import Flask, request
from handlers import CatAPIHandler, TextProcessor, TwilioMessageHandler

import random

app = Flask(__name__)
twilio = TwilioMessageHandler()
cat_api = CatAPIHandler()
text_processor = TextProcessor()


@app.route("/sms", methods=["POST"])
def sms_reply():
    """Respond to incoming messages."""
    if request.method == "POST":
        incoming_message = request.values.get("Body", None)
        incoming_number = request.values.get("From", None)

        print(f"Message received: {incoming_message}")

        # Strip all punctuation, lowercase all characters, and tokenize by word
        query = text_processor.preprocess_text(incoming_message)
        random.shuffle(query)

        # Find keywords in query to determine appropriate response
        if "cat" in query or "kitty" in query:
            # if "fact" in query:
            #     kitty_image_url, message = cat_api.get_cat_image(get_fact=True)
            # else:
            wanted_category = None
            wanted_breed = None
            for keyword in query:
                if keyword in cat_api.CATEGORY_IDS:
                    wanted_category = keyword
                    break
                elif keyword in cat_api.BREED_IDS:
                    wanted_breed = keyword
                    break
            kitty_image_url, message = cat_api.get_cat_image(
                category=wanted_category, breed=wanted_breed
            )
        else:
            kitty_image_url, message = None, "Sorry, I didn't understand your request."

        # Send message and get the message sid
        message_sid = twilio.send_message(
            receiving_number=incoming_number,
            text_message=message,
            image_url=kitty_image_url,
        )

        # Create JSON response.
        response = {
            "incoming_message": incoming_message,
            "receiving_number": incoming_number,
            "outgoing_message": message,
            "image_url": kitty_image_url,
            "status": message_sid,
        }
        return response


if __name__ == "__main__":
    app.run()
