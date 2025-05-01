from uuid import uuid5
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=15)
    secret_key = models.TextField()
    salt = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class FileModel(models.Model):
    file_id = models.CharField(max_length=500)
    file_url = models.FileField(upload_to="encrypted/")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file_id
