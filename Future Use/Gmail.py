import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import sys


def send_email(subject, body, sender_email, receiver_email, password):
    """Sends an email using Gmail SMTP server."""
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    part1 = MIMEText(body, "plain")
    message.attach(part1)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)


def main():
    # Logging configuration
    logging.basicConfig(filename='myprogram.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Your program logic here
    # ...

    try:
        # Your program's main code
        pass
    except Exception as e:
        logging.exception("Program encountered an error:")
    finally:
        # Get log content
        with open('myprogram.log', 'r') as f:
            log_content = f.read()

        # Send email notification
        sender_email = "your_email@gmail.com"
        receiver_email = "recipient_email@gmail.com"
        password = "your_gmail_app_password"  # Use app password for security
        subject = "Program Termination Notification"
        body = f"Program terminated. Log details:\n\n{log_content}"
        send_email(subject, body, sender_email, receiver_email, password)


if __name__ == "__main__":
    main()
