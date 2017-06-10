from django.utils.deprecation import MiddlewareMixin
import os
import dotenv
from twilio.rest import Client

dotenv.load()

class SMSMiddleware(object):
    def process_request(self, request):
        args = request.POST or request.GET
        request.is_sms = args and args.get('MessageSid')

class SMSMiddlewareUpgraded(MiddlewareMixin, SMSMiddleware):
  pass

def load_twilio_config():
    twilio_account_sid = dotenv.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = dotenv.get('TWILIO_AUTH_TOKEN')
    twilio_number = dotenv.get('TWILIO_NUMBER')

    if not all([twilio_account_sid, twilio_auth_token, twilio_number]):
        logger.error(NOT_CONFIGURED_MESSAGE)
        raise MiddlewareNotUsed

    return (twilio_number, twilio_account_sid, twilio_auth_token)

class MessageClient(object):
    def __init__(self):
        (twilio_number, twilio_account_sid,
         twilio_auth_token) = load_twilio_config()

        self.twilio_number = twilio_number
        self.twilio_client = Client(twilio_account_sid,
                                              twilio_auth_token)

        # self.twilio_client.messages.create(
        #     to='+447753314014',
        #     from_='+447400344583',
        #     body="Hi Gam, it's that time of the week for you to fill in your questionnaire, is now a good time?"
        # )

        # print 'this ran'

    def send_message(self, message, patient_number):
        self.twilio_client.messages.create(body=message, to=patient_number,
                                           from_='+447400344583',
                                           )


class TwilioMessage(object):
    def __init__(self):
        self.client = MessageClient()

    def send_sms(self, message_to_send, phone_number):
        self.client.send_message(message_to_send, phone_number)

        return None

