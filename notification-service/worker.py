from dotenv import load_dotenv
from flask import jsonify
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

# def send_sms(to, message):
#     # Simulate sending SMS (replace with actual integration logic)
#     print(f"Sending SMS to {to}: {message}")
#     time.sleep(2)  # Simulate delay
#     return f"Notification sent to {to}"

def send_sms(to_phone, message_body):
    try:
        # Get recipient phone number and message from the request
        # data = request.json
        # to_phone = data.get("to")
        # message_body = data.get("message")
        
        # Check for required fields
        if not to_phone or not message_body:
            return jsonify({"error": "Missing 'to' or 'message' field"}), 400
        
        # Send the SMS using Twilio
        client.messages.create(
            to=to_phone,
            from_=TWILIO_PHONE_NUMBER,
            body=message_body
        )
        
        # Return the Twilio message SID as confirmation
        print(f"SMS sent to {to_phone}")
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")

 
