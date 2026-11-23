FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY server.py ./server.py
COPY feast_api ./feast_api
RUN mkdir -p /data && chmod 700 /data

EXPOSE 8000
CMD ["python", "server.py"]
