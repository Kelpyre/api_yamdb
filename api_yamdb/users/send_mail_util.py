from django.core.mail import send_mail


def send_password_mail(mail, password):
    send_mail(
        'Пароль доступа для yamdb',
        f'Ваш пароль: {password}',
        'from@example.com',
        [mail],
        fail_silently=False,
    )
