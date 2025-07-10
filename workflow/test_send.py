
import resend

import os
from dotenv import load_dotenv
load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

with open("Pragyam.html", "r") as f:
    html = f.read()

params: resend.Emails.SendParams = {
    "from": "Food For Thou <newsletter@foodforthou.com>",
    "to": ["pragyamtiwari@gmail.com"],
    "subject": "07/09/2025",
    "html": html,
}

email = resend.Emails.send(params)
print(email)