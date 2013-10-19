from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

######Temporary logger######
import logging
############


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password1 = forms.CharField(
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        widget = forms.PasswordInput()
    )

    logging.basicConfig(filename='example.log',level=logging.DEBUG,)
#Password Verification
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']

            logging.info("Password1: %s" % password1)
            logging.info("Password2: %s" % password2)

            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

#Username Validation
    def clean_username(self):
        username = self.cleaned_data['username']

        logging.info("Username received by the clean_username function: %s" % username)
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Usernames can contain alphanumeric \
                    characters and underscore \'_\'')
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            logging.info("No matching username found. All good!")
            return username
        raise forms.ValidationError('Username is already taken')


