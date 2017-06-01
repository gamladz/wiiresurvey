import os
import dotenv
from twilio.rest import Client

dotenv.load()

account_sid = dotenv.get('TWILIO_ACCOUNT_SID')
auth_token = dotenv.get('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

client.messages.create(
    to=dotenv.get('MY_PHONE_NUMBER'),
    from_="+447400344583",
    body="Hi Kurren, it's that time of the week for you to fill in your questionnaire, is now a good time?"
)
