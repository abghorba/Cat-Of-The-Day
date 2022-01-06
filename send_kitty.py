import requests

from config import CAT_API_KEY, MY_NUMBER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
from twilio.rest import Client

CAT_API_URL = 'https://api.thecatapi.com/v1/images/search'

my_headers = {'x-api-key': CAT_API_KEY}
response = requests.get(url=CAT_API_URL, headers=my_headers)
data = response.json()
kitty_image_url = data[0]['url']

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) 

message = client.messages.create(
    from_=TWILIO_PHONE_NUMBER,
    to=MY_NUMBER,
    body='Here is your kitty of the day!',
    media_url=[kitty_image_url]
)
print(message.sid)