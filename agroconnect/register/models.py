from django.db import models
from django.contrib.auth.models import User

# Create a profile model to store additional information like mobile number
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class Register(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, blank=False, unique=True)
    email = models.EmailField(max_length=100, blank=False, unique=True)
    mobile = models.PositiveIntegerField(blank=False, unique=True)
    password = models.CharField(max_length=15)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    
    def __str__(self):
        return self.username + "-" + self.email