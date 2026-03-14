FROM python:3.11-slim

# Simulate server identity
ENV SERVER_NAME=APPWIN01
ENV DOMAIN_JOINED=true
ENV DOMAIN_NAME=CORP.NBFC.LOCAL
ENV CPU_USAGE=45
ENV MEMORY_USAGE=60
ENV APP_PORT=8080

RUN pip install flask

WORKDIR /app

COPY server.py .

CMD ["python", "server.py"]