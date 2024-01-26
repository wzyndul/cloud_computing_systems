from django.db import models
from django.contrib.auth.models import User


class UserActivityLog(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'User Activity Logs'


class FileActivityLog(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=100)
    file_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'File Activity Logs'
