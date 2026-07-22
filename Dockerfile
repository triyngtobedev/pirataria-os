FROM python:3.12-slim

WORKDIR /app

ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD flask db upgrade && gunicorn --bind 0.0.0.0:$PORT run:app
