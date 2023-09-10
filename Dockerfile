FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip setuptools

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["gunicorn", "--forwarded-allow-ips", "*", "-k", "uvicorn.workers.UvicornWorker", "nulland.main:app"]
