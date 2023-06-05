from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_activation_code(email, activation_code):
    context = {
        'text_detail' : 'Cпасибо за регистрацию',
        'email': email,
        'domain': 'http://localhost:8000',
        'activation_code': activation_code
    }
    mes_html = render_to_string('index.html', context)
    message = strip_tags(mes_html)

    send_mail('Account activation', message, 'admin@gmail.com', [email],html_message=mes_html ,fail_silently=False)