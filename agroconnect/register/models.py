from django.db import models
from django.contrib.auth.models import User

# Create a profile model to store additional information like mobile number
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
