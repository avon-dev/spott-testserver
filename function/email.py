
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



def authenticate(user_type, **authenticate_kwargs):
    try:
        user = User.objects.get(email = authenticate_kwargs[self.username_field],\
         user_type = user_type, is_active = True)
    except User.DoesNotExist as e:
        user = None
    else:
        if not check_password(authenticate_kwargs['password'],self.user.password):
            user = None
    return user

# class asd:
#     aa = "a"
