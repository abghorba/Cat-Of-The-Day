from flask import Flask, request
from handlers import CatAPIHandler, TwilioMessageHandler

import re

app = Flask(__name__)
twilio = TwilioMessageHandler()
cat_api = CatAPIHandler()

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming messages."""
    if request.method == "POST":
        incoming_message = request.values.get('Body', None)
        incoming_number = request.values.get('From', None)

        print(f'Message received: {incoming_message}')

        # Strip all punctuation, tokenize, and transform into a set
        query = re.sub(r'[^\w\s]', '', incoming_message)
        query = query.lower()
        query = query.split(" ")
        query = set(query)

        # Find keywords in query to determine appropriate response
        if 'cat' in query or 'kitty' in query:
            if 'fact' in query:
                kitty_image_url, message = cat_api.get_cat_image(get_fact=True)
            elif 'sunglasses' in query:
                kitty_image_url, message = cat_api.get_cat_image(category="sunglasses")
            elif 'boxes' in query or 'box' in query:
                kitty_image_url, message = cat_api.get_cat_image(category="boxes")
            elif 'clothes' in query:
                kitty_image_url, message = cat_api.get_cat_image(category="clothes")
            elif 'hats' in query or 'hat' in query:
                kitty_image_url, message = cat_api.get_cat_image(category="hats")
            elif 'sinks' in query or 'sink' in query:
                kitty_image_url, message = cat_api.get_cat_image(category="sinks")
            elif 'space' in query:
                kitty_image_url, message = cat_api.get_cat_image(category="space")
            elif 'ties' in query or 'tie' in query:
                kitty_image_url, message = cat_api.get_cat_image(category="ties")
            else:
                kitty_image_url, message = cat_api.get_cat_image()
        else:
            kitty_image_url, message = None, "Sorry, I didn't understand your request."

        # Send message
        message_status = twilio.send_message(
                receving_number=incoming_number,
                text_message=message,
                image_url=kitty_image_url
                )

        # Create JSON response.
        response = {
            "incoming_message": incoming_message,
            "receiving_number": incoming_number,
            "outgoing_message": message,
            "image_url": kitty_image_url,
            "status": message_status
        }
        return response

if __name__ == "__main__":
    app.run()
