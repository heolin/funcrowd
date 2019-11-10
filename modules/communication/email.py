from django.core.mail import send_mail
from funcrowd.settings import EMAIL_HOST_USER


class EmailHelper:
    @staticmethod
    def _send(email, subject, body):
        send_mail(subject, body, EMAIL_HOST_USER, [email])

    def send_activation_email(end_worker, token):
        EmailHelper._send(
            end_worker.email,
            'funcrowd activation token',
            f'lol tu masz token: \"{token.token}\"'
        )
