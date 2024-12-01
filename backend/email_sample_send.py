from cryptography.hazmat.backends.openssl import backend
from django.conf import settings
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created, pre_password_reset, post_password_reset



def emails_send(email_list: list, sample: str):
    context = {
        'sample': sample
    }
    print(context['sample'])
    # render email text
    email_html_message = render_to_string('email/email_sample_send.html', context)
    email_plaintext_message = render_to_string('email/email_sample_send.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Рассылка от {title}".format(title="AutoCRM"),
        # message:
        email_plaintext_message,
        # from:
        EMAIL_HOST_USER,
        # to:
        email_list
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()