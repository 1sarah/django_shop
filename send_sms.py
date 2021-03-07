import os
import africastalking
from django_shop.settings import env


from twilio.rest import Client

def send(message, to_phone_number):
    # the following line needs your Twilio Account SID and Auth Token
    ACCOUNT_SID = env.str('ACCOUNT_SID')
    TOKEN = env.str('TOKEN')
    client = Client(ACCOUNT_SID, TOKEN)

    # change the "from_" number to your Twilio number and the "to" number
    # to the phone number you signed up for Twilio with, or upgrade your
    # account to send SMS to any phone number
    client.messages.create(to=to_phone_number, 
                        from_="+14804050909", 
                        body=message)

def send_sms(message, recipients):
    username = "sandbox"
    api_key = env.str('SMS_API_KEY')
    africastalking.initialize(username, api_key)
    sms = africastalking.SMS

    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as e:
        print(f"======================Something went wrong {e}===================================")