from django.core.mail import send_mail
from funcrowd.settings import EMAIL_HOST_USER


class EmailHelper:
    @staticmethod
    def _send(email, subject, body):
        send_mail(subject, "", EMAIL_HOST_USER, [email], html_message=body)

    @staticmethod
    def send_activation_email(end_worker, token):
        token_value = token.token
        EmailHelper._send(
            end_worker.email,
            'Aktywacja konta SpaceCalc',
            f"""
                <p>Witaj {end_worker.username}!</p>
                <p>Dziękujemy za rejestrację na portalu <a target="_blank" href="https://spacecalc-course.herokuapp.com/#/activation?activationToken={token_value}">https://spacecalc-course.herokuapp.com/#/activation?activationToken={token}</a>
                </p>
                <p>Jeśli link nie działa, skopiuj go i wklej w okno adresu przeglądarki.</p>
                <p>Jeśli nie oczekiwałeś/łaś na tą wiadomość, oznacza to że ktoś podał twój email w trakcie rejestracji. W takim przypadku zignoruj tę wiadomość.</p>
                <p>Wiadomość została wygenerowana automatycznie, nie odpowiadaj na nią.</p>
                <p>Powodzenia w kursie!<br/>Zespół Space Calc</p>
            """
        )

    @staticmethod
    def send_reset_password_email(end_worker, token):
        token_value = token.token
        EmailHelper._send(
            end_worker.email,
            'Reset hasła SpaceCalc',
            f"""
                <p>Cześć {end_worker.username}!</p>
                <p>Otrzymaliśmy prośbę dotyczącą zresetowania Twojego hasła na portalu  https://spacecalc-course.herokuapp.com/. Kliknij w link, aby ustawić nowe hasło dla swojego konta: 
                    <a target="_blank" href="https://spacecalc-course.herokuapp.com/#/reset_password_token?resetPasswordToken={token_value}">https://spacecalc-course.herokuapp.com/#/reset_password_token?resetPasswordToken={token}</a>
                </p>
                <p>Pozdrawiamy,<br/>Zespół Space Calc</p>
            """
        )
