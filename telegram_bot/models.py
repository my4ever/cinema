from django.db import models


class TelegramUser(models.Model):
    user_id = models.IntegerField()
    last_command = models.CharField(max_length=40)
    last_movie = models.CharField(max_length=100)
