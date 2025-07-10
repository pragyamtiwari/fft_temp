
import resend

import os
from dotenv import load_dotenv
load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def send_story(email, html):
    params: resend.Emails.SendParams = {
        "from": "Food For Thou <newsletter@foodforthou.com>",
        "to": [email],
        "subject": "07/09/2025",
        "html": html,
    }

    email = resend.Emails.send(params)
    print(email)