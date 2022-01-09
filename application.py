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
        message = re.sub(r'[^\w\s]', '', incoming_message)
        message = message.lower()
        message = message.split(" ")
        message = set(message)

        # Find keywords in message to determine appropriate response
        if 'cat' in message or 'kitty' in message:
            if 'fact' in message:
                kitty_image_url, kitty_fact = cat_api.get_cat_image(get_fact=True)
            elif 'sunglasses' in message:
                kitty_image_url, kitty_fact = cat_api.get_cat_image(category="sunglasses")
            elif 'boxes' in message or 'box' in message:
                kitty_image_url, kitty_fact = cat_api.get_cat_image(category="boxes")
            elif 'clothes' in message:
                kitty_image_url, kitty_fact = cat_api.get_cat_image(category="clothes")
            elif 'hats' in message or 'hat' in message:
                kitty_image_url, kitty_fact = cat_api.get_cat_image(category="hats")
            elif 'sinks' in message or 'sink' in message:
                kitty_image_url, kitty_fact = cat_api.get_cat_image(category="sinks")
            elif 'space' in message:
                kitty_image_url, kitty_fact = cat_api.get_cat_image(category="space")
            elif 'ties' in message or 'tie' in message:
                kitty_image_url, kitty_fact = cat_api.get_cat_image(category="ties")
            else:
                kitty_image_url, kitty_fact = cat_api.get_cat_image()
        else:
            kitty_image_url, kitty_fact = None, "Invalid command."

        # Send message
        twilio.send_message(
            receving_number=incoming_number,
            text_message=kitty_fact,
            image_url=kitty_image_url
        )

        return "Message sent!"

if __name__ == "__main__":
    app.run()
    