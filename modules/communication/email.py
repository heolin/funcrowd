from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from funcrowd.settings import SENDGRID_API_KEY


class EmailSender:
    def __init__(self):
        self.sg = SendGridAPIClient(SENDGRID_API_KEY)

    def send(self, sender, email, subject, body):
        message = Mail(
            from_email = sender,
            to_emails = email,
            subject = subject,
            html_content = body)
        self.sg.send(message)
