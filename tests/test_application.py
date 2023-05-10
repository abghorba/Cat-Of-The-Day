import pytest

from application import app

app.config["TESTING"] = True


class TestAppRouteSMS:
    @pytest.mark.parametrize(
        "message,expected_response",
        [
            (
                {"Body": "", "From": "+1234567890"},
                [
                    '"incoming_message": ""',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Sorry, I didn\'t understand your request."',
                    '"image_url": null',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Hello, world!", "From": "+1234567890"},
                [
                    '"incoming_message": "Hello, world!"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Sorry, I didn\'t understand your request."',
                    '"image_url": null',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Cat?", "From": "+1234567890"},
                [
                    '"incoming_message": "Cat?"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Sorry, I didn\'t understand your request."',
                    '"image_url": null',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Show me", "From": "+1234567890"},
                [
                    '"incoming_message": "Show me"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Sorry, I didn\'t understand your request."',
                    '"image_url": null',
                    '"status": ',
                ],
            ),
            (
                {
                    "Body": "This is purposely a very long string just so I can test the boundaries of the application. "
                    "Did it work? Hopefully so! Otherwise, back to the start.",
                    "From": "+1234567890",
                },
                [
                    '"incoming_message": "This is purposely a very long string just so I can test the boundaries of '
                    'the application. Did it work? Hopefully so! Otherwise, back to the start."',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Please limit your request to less than 100 characters."',
                    '"image_url": null',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Send me an american shorthair", "From": "+1234567890"},
                [
                    '"incoming_message": "Send me an american shorthair"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Here is a American Shorthair cat!"',
                    '"image_url": "https://cdn2.thecatapi.com/images/',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Show me a picture of a siamese cat", "From": "+1234567890"},
                [
                    '"incoming_message": "Show me a picture of a siamese cat"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Here is a Siamese cat!"',
                    '"image_url": "https://cdn2.thecatapi.com/images/',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Give me a norwegian forest cat", "From": "+1234567890"},
                [
                    '"incoming_message": "Give me a norwegian forest cat"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Here is a Norwegian Forest Cat cat!"',
                    '"image_url": "https://cdn2.thecatapi.com/images/',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Let me see a cat wearing sunglasses", "From": "+1234567890"},
                [
                    '"incoming_message": "Let me see a cat wearing sunglasses"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Here is a cat wearing sunglasses!"',
                    '"image_url": "https://cdn2.thecatapi.com/images/',
                    '"status": ',
                ],
            ),
            (
                {"Body": "I want to get a kitty wearing some clothes", "From": "+1234567890"},
                [
                    '"incoming_message": "I want to get a kitty wearing some clothes"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Here is a cat wearing clothes!"',
                    '"image_url": "https://cdn2.thecatapi.com/images/',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Send me a cat sitting inside a box", "From": "+1234567890"},
                [
                    '"incoming_message": "Send me a cat sitting inside a box"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Here is a cat in a box!"',
                    '"image_url": "https://cdn2.thecatapi.com/images/',
                    '"status": ',
                ],
            ),
            (
                {"Body": "I want to receive a cat chilling in a sink", "From": "+1234567890"},
                [
                    '"incoming_message": "I want to receive a cat chilling in a sink"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Here is a cat in a sink!"',
                    '"image_url": "https://cdn2.thecatapi.com/images/',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Show me a cat in space", "From": "+1234567890"},
                [
                    '"incoming_message": "Show me a cat in space"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Here is a cat in space!"',
                    '"image_url": "https://cdn2.thecatapi.com/images/',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Give me a cat in a hat", "From": "+1234567890"},
                [
                    '"incoming_message": "Give me a cat in a hat"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Here is a cat wearing a hat!"',
                    '"image_url": "https://cdn2.thecatapi.com/images/',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Let me see a cat wearing a tie, please!", "From": "+1234567890"},
                [
                    '"incoming_message": "Let me see a cat wearing a tie, please!"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Here is a cat wearing a tie!"',
                    '"image_url": "https://cdn2.thecatapi.com/images/',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Let me see a bengal cat wearing sunglasses", "From": "+1234567890"},
                [
                    '"incoming_message": "Let me see a bengal cat wearing sunglasses"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Here is a cat wearing sunglasses!"',
                    '"image_url": "https://cdn2.thecatapi.com/images/',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Let me see an american shorthair in a box.", "From": "+1234567890"},
                [
                    '"incoming_message": "Let me see an american shorthair in a box."',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Here is a cat in a box!"',
                    '"image_url": "https://cdn2.thecatapi.com/images/',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Show me a cat", "From": "+1234567890"},
                [
                    '"incoming_message": "Show me a cat"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Here is a random cat!"',
                    '"image_url": "https://cdn2.thecatapi.com/images/',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Send a cat", "From": "+1234567890"},
                [
                    '"incoming_message": "Send a cat"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Here is a random cat!"',
                    '"image_url": "https://cdn2.thecatapi.com/images/',
                    '"status": ',
                ],
            ),
            (
                {"Body": "Send a kitty cat", "From": "+1234567890"},
                [
                    '"incoming_message": "Send a kitty cat"',
                    '"receiving_number": "+1234567890"',
                    '"outgoing_message": "Here is a random cat!"',
                    '"image_url": "https://cdn2.thecatapi.com/images/',
                    '"status": ',
                ],
            ),
        ],
    )
    def test_sms_reply(self, message, expected_response):
        """Tests the /sms app route."""

        response = app.test_client().post("/sms", data=message)
        data = response.data.decode("utf-8")

        for expected_str in expected_response:
            if "image_url" in expected_str:
                assert expected_str in data or "media.tumblr.com" in data

            else:
                assert expected_str in data
