FROM python:3.9-slim

WORKDIR /app


COPY . /app

# Install dependencies (Flask, Boto3, etc.)
RUN pip install --no-cache-dir -r app/requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
