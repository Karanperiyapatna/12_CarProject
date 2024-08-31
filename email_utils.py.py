# email_utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_confirmation_email(email, vehicle_type, regNumber):
    sender_email = "periyapatnakaran@gmail.com"  # Replace with your email address
    sender_password = "your_password"  # Replace with your email password
    subject = "Vehicle Booking Confirmation"
    body = f"Your {vehicle_type} with registration number {regNumber} has been booked successfully!"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('localhost', 1025)  # Use local SMTP server
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
