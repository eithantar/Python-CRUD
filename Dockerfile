FROM python:3.12-slim

WORKDIR /app

# mysql-connector-python is pure Python, so no system MySQL libraries are needed.
# Install dependencies first so this layer is cached between code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    PYTHONUNBUFFERED=1

CMD ["flask", "run"]
