import os
from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()

TWILIO_ACCOUNT_SID=os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN=os.getenv('TWILIO_AUTH_TOKEN')

client=Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)

#----------------------------------------------------------------
# Twilio Connection
#----------------------------------------------------------------

def send_message(to:str , message:str)->None:
    _=client.messages.create(
        from_=os.getenv('FROM'),
        body=message,
        to=to
    )
