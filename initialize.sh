#!/bin/sh

if [ ! -d "env" ]; then
    echo "Creating virtual environment: env"
    python3 -m venv env
    source env/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "Done!"
fi

CAT_API_KEY=""
TWILIO_ACCOUNT_SID=""
TWILIO_AUTH_TOKEN=""
TWILIO_PHONE_NUMBER=""
MY_NUMBER=""
if [ ! -f ".env" ]; then
    echo "Creating .env file to store environment variables..."
    touch .env
    echo "CAT_API_KEY = \"$CAT_API_KEY\"" >> .env
    echo "TWILIO_ACCOUNT_SID = \"$TWILIO_ACCOUNT_SID\"" >> .env
    echo "TWILIO_AUTH_TOKEN = \"$TWILIO_AUTH_TOKEN\"" >> .env
    echo "TWILIO_PHONE_NUMBER = \"$TWILIO_PHONE_NUMBER\"" >> .env
    echo "MY_NUMBER = \"$MY_NUMBER\"" >> .env
    echo "Done!"
fi