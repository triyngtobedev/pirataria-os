FROM python:3.12-slim

WORKDIR /app

ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends libmagic1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD flask db upgrade 2>/dev/null || flask db stamp head && flask db upgrade && gunicorn --bind 0.0.0.0:$PORT run:app
