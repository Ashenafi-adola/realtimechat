from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username
    
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reciever = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    sent_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[:20]