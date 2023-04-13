from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from Accounts.models import User
from Cyberfolio.settings import AUTH_PASSWORD_VALIDATORS


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        help_texts = {
            'email': None,
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # for fieldname in ['password2',]:
        self.fields['password2'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['email'].help_text = None


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class RandomForm(forms.Form):
    name = forms.CharField (max_length=100)
    surName = forms.CharField(max_length=100)
    surSurName = forms.CharField(max_length=100)

