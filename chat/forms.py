from django.forms import ModelForm
from . models import CustomUser, Message

class CustomUserCreationForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
    