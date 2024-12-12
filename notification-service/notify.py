from dotenv import load_dotenv
from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
from worker import send_sms
import os



# Initialize Flask app
app = Flask(__name__)

# Import env variables

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

# Connect to Redis and set up a queue
redis_conn = Redis(REDIS_HOST, REDIS_PORT)
queue = Queue(connection=redis_conn)

@app.route('/notify', methods=['POST'])
def notify():
    print("Notification endpoint called!")
    data = request.get_json()
    print(f"Received data: {data}")

    if not data or 'to' not in data or 'message' not in data:
        return jsonify({"error": "Invalid request data"}), 400

    phone = data['to']
    message = data['message']

    # Add the job to the queue
    try:
        job = queue.enqueue(send_sms, phone, message)
        return jsonify({"status": "Job queued", "job_id": job.id}), 200
    except Exception as e:
        print(f"Error enqueueing job: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3002)
