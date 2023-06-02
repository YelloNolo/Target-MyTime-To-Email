import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv('.env')

# Email Details
receiver_emails_str = os.getenv('receiver_emails')
receiver_emails = eval(receiver_emails_str)
subject = os.getenv('subject')

# SMTP server details
smtp_server = os.getenv('smtp_server')
smtp_port_str = os.getenv('smtp_port')
smtp_port = int(smtp_port_str)
smtp_username = os.getenv('smtp_username')
smtp_password = os.getenv('smtp_password')

schedule_file_path = os.getenv('schedule_file_path')

# Read the content from the text file
with open(schedule_file_path, 'r') as file:
    file_content = file.read()

# Create a multipart message
msg = EmailMessage()
msg['From'] = smtp_username
msg['To'] = ', '.join(receiver_emails)
msg['Subject'] = subject

# Add body to the email
msg.set_content(file_content)

def send():
    # Create SMTP session
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS encryption
            server.login(smtp_username, smtp_password)  # Login to the SMTP server
            server.send_message(msg)  # Send the email
        print('Email sent successfully!')
    except smtplib.SMTPException as e:
        print('Error occurred while sending email:', str(e))

print("--------------------")
print("Email From: ", smtp_username)
print("Email TO: ", ', '.join(receiver_emails))
print("--------------------")

# Confirm sending email
while True:
    user_choice = input("Send Email? (y/n): ")
    if user_choice.lower() == 'y':
        send()
        break
    elif user_choice.lower() == 'n':
        # User chose not to continue
        print("--------------------")
        quit()
    else:
        # Invalid choice
        print("--------------------\nInvalid choice. Please try again.")
