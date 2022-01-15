from flask import Flask, request
from handlers import CatAPIHandler, TextProcessor, TwilioMessageHandler

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

        # Clean the incoming message to be usable
        query = text_processor.clean_text(incoming_message)

        # Find keywords in query to determine appropriate response
        if "cat" in query or "kitty" in query:
            # Check if any of the breeds are in query
            requested_breed = text_processor.find_keywords_in_text(
                cat_api.BREED_IDS, query
            )

            # Check if any of the categories are in query
            requested_category = text_processor.find_keywords_in_text(
                cat_api.CATEGORY_IDS, query
            )

            # Make the API call
            cat_image_url, message = cat_api.get_cat_image(
                category=requested_category, breed=requested_breed
            )

        else:
            cat_image_url, message = None, "Sorry, I didn't understand your request."

        # Send message and get the message sid
        message_sid = twilio.send_message(
            receiving_number=incoming_number,
            text_message=message,
            image_url=cat_image_url,
        )

        # Create JSON response.
        response = {
            "incoming_message": incoming_message,
            "receiving_number": incoming_number,
            "outgoing_message": message,
            "image_url": cat_image_url,
            "status": message_sid,
        }
        return response


if __name__ == "__main__":
    app.run()
