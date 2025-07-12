import resend

import os
from dotenv import load_dotenv
load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

def test():
    params = {
        "from": "Food For Thou <auth@foodforthou.com>",
        "to": ["pragyamtiwari@gmail.com"],
        "subject": "Food For Thou Authentication",
        "html": f"<strong>Why isn't this working</strong>",
    }
    email = resend.Emails.send(params)
    print(email)

if __name__ == "__main__":
    test()
    