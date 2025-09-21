import asyncio
from aiosmtpd.controller import Controller
import requests
import os

MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")


class MailgunHandler:
    async def handle_DATA(self, server, session, envelope):
        try:
            response = requests.post(
                f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
                auth=("api", MAILGUN_API_KEY),
                data={
                    "from": envelope.mail_from,
                    "to": ", ".join(envelope.rcpt_tos),
                    "subject": "Message from OpenProject",
                    "text": envelope.content.decode("utf-8", errors="replace"),
                },
            )
            if response.status_code == 200:
                return "250 Message accepted for delivery"
            else:
                print(f"Mailgun error: {response.status_code} {response.text}")
                return "550 Failed to relay message"
        except Exception as e:
            print(f"Relay exception: {e}")
            return "451 Temporary local problem"


if __name__ == "__main__":
    hostname = "0.0.0.0"
    port = int(os.getenv("RELAY_PORT", "2525"))
    controller = Controller(MailgunHandler(), hostname=hostname, port=port)
    controller.start()
    print(f"SMTP relay listening on {hostname}:{port}")
    asyncio.get_event_loop().run_forever()
