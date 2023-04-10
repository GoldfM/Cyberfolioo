from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from Accounts.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'spec' ,'password1', 'password2')
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
            'phone_number': None,
            'spec': None
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # for fieldname in ['password2']:
        self.fields['password2'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number')
