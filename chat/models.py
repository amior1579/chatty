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
    


class channelLayers(models.Model):
    client1 = models.ForeignKey(UserAuth, related_name='client1', on_delete=models.CASCADE)
    client2 = models.ForeignKey(UserAuth, related_name='client2', on_delete=models.CASCADE, null=True)
    room_name = models.TextField()

    # def __str__(self):
    #     return f'{self.client1.username} to {self.client2.username}'
    