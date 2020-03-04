
from django.core.mail import EmailMessage

def is_valid(addr):
    import re
    if re.match('(^[a-zA-Z-0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', addr):
        return False
    else:
        return True


def email_setting(self, email_contents, random, email):
    auth_code_text = "인증코드: "
    subject = email_contents
    message = auth_code_text + random

    return EmailMessage(subject,message,to=[email])

# class asd:
#     aa = "a"
