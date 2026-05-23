from django.forms import ModelForm
from django.forms import TextInput, FileInput, Textarea, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from . models import CustomUser, Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username","email", "profile", "password1", "password2"]
        widgets = {
            'username': TextInput(attrs={
                'class':"form-control",
            }),
            'email': EmailInput(attrs={
                'class':"form-control"
            }),
            'profile': FileInput(attrs={
                'class': "profile",
            }),
            'password1': PasswordInput(attrs={
                'class': 'form-control'
            }),
            'password2': PasswordInput(attrs={
                'class': 'form-control'
            })

        }
    def save(self, commit = True):
        user = super().save(commit=False)
        user.profile = self.cleaned_data['profile']
        if commit:
            user.save()
        return user

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'name': 'message',
                'style': "width: 100%",
                'data-custom': 'some-value',
                'placeholder': "Type message here..."
            }),
        }
    