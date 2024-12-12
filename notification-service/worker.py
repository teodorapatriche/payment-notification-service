from dotenv import load_dotenv
from twilio.rest import Client
import os

# Load environment variables
load_dotenv()

# Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
    raise ValueError("Twilio credentials are not set in the environment variables.")

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to_phone, message_body):
    try:
        if not to_phone or not message_body:
            raise ValueError("Missing 'to' or 'message' field")
        
        # Send the SMS using Twilio
        message = client.messages.create(
            to=to_phone,
            from_=TWILIO_PHONE_NUMBER,
            body=message_body
        )
        
        # Return the Twilio message SID as confirmation
        print(f"SMS sent to {to_phone}")
        return {
            "status": "success",
            "message_sid": message.sid
        }
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")
        raise  # Re-raise the exception to mark the job as failed