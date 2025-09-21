FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN pip install aiosmtpd requests

COPY relay.py /app/relay.py

# Expose SMTP port
EXPOSE 2525

CMD ["python", "relay.py"]
