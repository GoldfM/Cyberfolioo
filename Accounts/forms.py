from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

#from Accounts.models import User
from Cyberfolio.settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # for fieldname in ['password2',]:
        self.fields['password2'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None
        list = ['Введите логин', 'Введите пароль', 'Повторите пароль']
        i=0
        for visible in self.visible_fields():
            print(visible)
            visible.field.widget.attrs['class'] = 'input enter-input'
            visible.field.widget.attrs['placeholder'] = list[i]
            i+=1


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', )


class firstForm(forms.Form):
    name = forms.CharField (max_length=100, widget=forms.TextInput(attrs={'class': 'input enter-input','placeholder':'Имя'}))
    surName = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input enter-input','placeholder':'Фамилия'}))
    surSurName = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input enter-input','placeholder':'Отчество (при наличии)'}))

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'input enter-input', 'placeholder':'Логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input enter-input', 'placeholder':'Пароль'}))
