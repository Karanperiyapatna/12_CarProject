import os

# Debugging: Print the environment variables
print(f"EMAIL_USER from env: {os.getenv('EMAIL_USER')}")
print(f"EMAIL_PASS from env: {os.getenv('EMAIL_PASS')}")

# MongoDB and Email sending logic
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pymongo import MongoClient

# MongoDB configuration
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['vehicle_rental']
collection = db['bookings']

# Query to get the status
document = collection.find_one({"status": 8})

if document:
    # Message details
    receiver_email_mail = document['Email ID']
    message_content = document['remark']
    # sender_email = os.getenv("EMAIL_USER")
    sender_email = "periyapatnakaran@gmail.com"
    receiver_email = receiver_email_mail
    # password = os.getenv("EMAIL_PASS")
    password = "egpb xvmh vntv iphd"

    # Debugging: Print the retrieved values
    print(f"Sender Email: {sender_email}")
    print(f"Receiver Email: {receiver_email}")
    print(f"Password is {'set' if password else 'not set'}")

    # Check if environment variables are set
    if not sender_email or not password:
        print("Error: EMAIL_USER and EMAIL_PASS environment variables must be set.")
        exit(1)

    # Setting up the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Booking Confirmation Mail - Hire Workers"

    # Adding the message content
    message.attach(MIMEText(message_content, 'plain'))

    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Port for TLS

    try:
        # Creating SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
else:
    print("No document found with status 7.")

# Optionally, log the message content back to MongoDB or another collection
log_collection = db['email_logs']
log_collection.insert_one({
    "message": message_content,
    "status": "sent"
})


'''


=================================================================================== Error ==================

import smtplib, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pymongo import MongoClient

# MongoDB configuration
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['vehicle_rental']
collection = db['bookings']

# Query to get the status
document = collection.find_one({"status": 7})

print(document)

if document:
    # Message details
    message_content = document['message']
    sender_email = "periyapatnakaran@gmail.com"
    receiver_email = "periyapatnakaran@outlook.com"
    password = "Karan#9986"

    # Setting up the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Automated Email"

    # Adding the message content
    message.attach(MIMEText(message_content, 'plain'))

    # Creating SMTP session
    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # Use your SMTP server and port
        server.starttls()
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
else:
    print("No document found with status 7.")

# Optionally, log the message content back to MongoDB or another collection
log_collection = db['email_logs']
log_collection.insert_one({
    "message": message_content,
    "status": "sent"
})

'''