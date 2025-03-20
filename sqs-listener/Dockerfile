FROM python:3.9

WORKDIR /sqs-listener

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY sqs-listener.py .

CMD ["python", "sqs-listener.py"]

