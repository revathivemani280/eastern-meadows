from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage

load_dotenv()

app = Flask(__name__)
CORS(app)

OWNER_EMAIL = os.getenv("OWNER_EMAIL")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


@app.route("/api/contact", methods=["POST"])
def contact():

    data = request.get_json()

    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not phone:
        return jsonify({
            "success": False,
            "message": "Name and phone number are required."
        }), 400

    email_message = EmailMessage()

    email_message["Subject"] = f"New Eastern Meadows Enquiry - {name}"
    email_message["From"] = EMAIL_ADDRESS
    email_message["To"] = OWNER_EMAIL
    email_message["Reply-To"] = email

    email_message.set_content(
        f"""
New enquiry received from Eastern Meadows website.

Name:
{name}

Phone:
{phone}

Email:
{email}

Message:
{message}
        """
    )

    try:

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            smtp.send_message(email_message)

        return jsonify({
            "success": True,
            "message": "Your enquiry has been submitted successfully."
        })

    except Exception as e:

        print("Email error:", e)

        return jsonify({
            "success": False,
            "message": "Unable to send enquiry."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )