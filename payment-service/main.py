from flask import Flask, request, jsonify
import stripe
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Stripe with secret key
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
print(f"Loaded Stripe API Key: {stripe.api_key}")


@app.route('/pay', methods=['POST'])
def process_payment():
    try:
        data = request.json
        amount = data['amount']
        currency = data['currency']
        
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=['card']
        )
        return jsonify({'clientSecret': payment_intent['client_secret']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
