import os
import dotenv
from twilio.rest import Client

dotenv.load()

account_sid = dotenv.get('TWILIO_ACCOUNT_SID')
auth_token = dotenv.get('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

client.messages.create(
    to="+447753314014",
    from_=dotenv.get('TWILIO_NUMBER'),
    body="Hi Gam, it's that time of the week for you to fill in your questionnaire, is now a good time?"
)

# Create a function,
# call it in the view
# Call send_sms in the view
