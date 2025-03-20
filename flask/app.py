import json
import re
import os
import boto3
from flask import Flask, request, jsonify
from botocore.exceptions import ClientError


#app = Flask(__name__)


sqs = boto3.client('sqs')

SQS_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/YOUR_ACCOUNT_ID/YOUR_QUEUE_NAME'

def get_token_from_env():
    # Get the token value from environment variables
    return os.getenv('token_value')

def validate_token(token):
    # Get the correct token from the environment variable
    valid_token = get_token_from_env()
    
    if valid_token and token == valid_token:
        return True
    return False

def validate_date(date_str):
    # Simple regex to check if the date has 4 text fields, e.g., "2025-03-19-12"
    date_pattern = r'^\d{4}-\d{2}-\d{2}-\d{2}$'
    return bool(re.match(date_pattern, date_str))

def send_message_to_sqs(payload):
    try:
        response = sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(payload)
        )
        print(f"Message sent to SQS with ID: {response['MessageId']}")
    except ClientError as e:
        print(f"Error sending message to SQS: {e}")

@app.route('/process_request', methods=['POST'])
def process_request():
    # Get the JSON data from the request payload
    data = request.get_json()

    # Extract token and date from the payload
    token = data.get('token')
    date_str = data.get('date')

    # Validate token
    if not validate_token(token):
        return jsonify({"error": "Invalid token"}), 401

    # Validate date format
    if not validate_date(date_str):
        return jsonify({"error": "Invalid date format"}), 400

    # If validation passes, publish the payload to SQS
    send_message_to_sqs(data)

    return jsonify({"message": "Request processed successfully"}), 200

if __name__ == '__main__':
    # Run the Flask app (default port is 5000)
    app.run(host='0.0.0.0', port=5000)

