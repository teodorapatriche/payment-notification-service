from flask import Flask, request, jsonify
import stripe
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

notification_url = os.getenv("NOTIFICATION_SERVICE_URL")
print(f"Notification URL from env: {notification_url}")

# Initialize Flask
app = Flask(__name__)

# Initialize Stripe with secret key
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
print(f"Loaded Stripe API Key: {stripe.api_key}")


def process_payment(data):
    try:
        amount = data['amount']
        currency = data['currency']
        
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=['card']
        )
        return {
            "status": "success",
            "client_secret": payment_intent.client_secret,
        }, 200
    except Exception as e:
        return {"status": "error", "error": str(e)}, 500
    #     return jsonify({'clientSecret': payment_intent['client_secret']}), 200
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

# Function to notify user
def notify_user(phone, message):
    
    try:
        if not notification_url:
            raise ValueError("Notification URL is not set")
        
        print(f"Notification URL: {notification_url}")
        print(f"Phone: {phone}")
        print(f"Message: {message}")

        notification_payload = {
            'to': phone,
            'message': message
        }
        
        
        response = requests.post(notification_url, json=notification_payload)
        print(f"Notification response status: {response.status_code}")
        print(f"Notification response text: {response.text}")
        if response.status_code == 200:
            return {"status": "success"}, 200
        else:
            return {
                "status": "error",
                "url" : f"Attempting to send notification to: {notification_url}",
                "error": f"Failed to send notification: {response.text}"
            }, 500
    except Exception as e:
        return {"status": "error", "error": str(e)}, 500

# Endpoint for handling payment requests    
@app.route('/pay', methods=['POST'])
def handle_payment():
    data = request.get_json()
    customer_phone = data.get('phone')
    print(customer_phone)
    amount = data.get('amount')
    currency = data.get('currency')

    # Step 1: Process Payment
    payment_result, status_code = process_payment(data)
    print(payment_result)
    if status_code != 200:
        return jsonify(payment_result), status_code
    
    notification_message = "Notification not sent."

    # Step 2: Notify User (if phone number is provided)
    if customer_phone:
        notification_message = f"Your payment of {amount/100:.2f} {currency.upper()} was successful."
        print(notification_message)
        notify_result, notify_status_code = notify_user(customer_phone, notification_message)
        if notify_status_code != 200:
            return jsonify({
                "error": "Payment succeeded, but notification failed.",
                "url" : f"Attempting to send notification to: {notification_url}",
                "notification_error": notify_result.get("error"),
                "clientSecret": payment_result.get("client_secret")
            }), 500

    # Final Response
    return jsonify(customer_phone, payment_result, notification_message), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
