import boto3
import time
import os
import json

# הגדרת משתנים סביבתיים
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 10))  # זמן בדיקה בברירת מחדל 10 שניות

# יצירת לקוחות של AWS
sqs = boto3.client('sqs')
s3 = boto3.client('s3')

def process_messages():
    """ מושך הודעות מ-SQS ומעלה אותן ל-S3 """
    while True:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=5
        )

        messages = response.get("Messages", [])
        
        for message in messages:
            body = message["Body"]
            message_id = message["MessageId"]
            
            # שמירת ההודעה ב-S3
            file_name = f"sqs_messages/{message_id}.json"  # תיקייה ייעודית ב-S3
            s3.put_object(Bucket=S3_BUCKET_NAME, Key=file_name, Body=body)
            print(f"Uploaded message {message_id} to S3 as {file_name}")
            
            # מחיקת ההודעה מהתור
            sqs.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=message["ReceiptHandle"])
            print(f"Deleted message {message_id} from SQS")
        
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    print("Starting SQS to S3 microservice...")
    process_messages()

