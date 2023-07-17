from django.db import models
from django.contrib.auth.models import AbstractUser

class UserAuth(AbstractUser):

    def __str__(self):
        return f'{self.username}'
    

class Message(models.Model):
    sender = models.ForeignKey(UserAuth, related_name='sender_message', on_delete=models.CASCADE)
    Receiver = models.ForeignKey(UserAuth, related_name='Receiver_message', on_delete=models.CASCADE, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} to {self.Receiver.username}'
    
    def last_10_messages(self):
        return Message.objects.order_by('-timestamp').all[:10]