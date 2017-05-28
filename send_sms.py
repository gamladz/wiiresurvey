import os
import dotenv
from twilio.rest import Client

dotenv.load()

account_sid = dotenv.get('TWILIO_ACCOUNT_SID')
auth_token = dotenv.get('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

client.messages.create(
    to=dotenv.get('MY_PHONE_NUMBER'),
    from_="+441938880001",
    body="Hello Finn"
)
