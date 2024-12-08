from flask import Flask, request, jsonify
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/notify', methods=['POST'])
def notify():
    try:
        # Get recipient phone number and message from the request
        data = request.json
        to_phone = data.get("to")
        message_body = data.get("message")
        
        # Check for required fields
        if not to_phone or not message_body:
            return jsonify({"error": "Missing 'to' or 'message' field"}), 400
        
        # Send the SMS using Twilio
        message = client.messages.create(
            to=to_phone,
            from_=TWILIO_PHONE_NUMBER,
            body=message_body
        )
        
        # Return the Twilio message SID as confirmation
        return jsonify({"message_sid": message.sid}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3002)
