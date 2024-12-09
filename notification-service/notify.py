from flask import Flask, request, jsonify



from redis import Redis
from rq import Queue
from worker import send_sms



# Initialize Flask app
app = Flask(__name__)

# Connect to Redis and set up a queue
redis_conn = Redis(host="localhost", port=6379)
queue = Queue(connection=redis_conn)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    if not data or 'to' not in data or 'message' not in data:
        return jsonify({"error": "Invalid request data"}), 400

    phone = data['to']
    message = data['message']

    # Add the job to the queue
    job = queue.enqueue(send_sms, phone, message)
    return jsonify({"status": "Job queued", "job_id": job.id}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3002)
