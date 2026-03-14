FROM python:3.11-slim

# Simulate PROBLEM server — domain dropped after patch
ENV SERVER_NAME=APPWIN02
ENV DOMAIN_JOINED=false
ENV DOMAIN_NAME=CORP.NBFC.LOCAL
ENV CPU_USAGE=92
ENV MEMORY_USAGE=87
ENV APP_PORT=8080

RUN pip install flask

WORKDIR /app

COPY server.py .

CMD ["python", "server.py"]