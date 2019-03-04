from django.core.mail import send_mail


class Controller:

    @staticmethod
    def send_activation_mail(token):
        if token:
            message = (
                "Hi,"
                "Please click on following link to activate your account.\n"
                "http://127.0.0.1:8000/trainer/register/?activation_token={0}"
            ).format(token)

            send_mail(
                'Activate your TrainOurStaff account',
                 message,
                'noreply@trainourstaff.com',
                ['kalpeshtawde@outlook.com'],
            )

        else:
            raise Exception("Token cannot be blank")