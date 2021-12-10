from django.db import models
from django.contrib.auth.models import User
import hashlib
from .utils import sendTransaction
import time
from datetime import datetime
from django.core.exceptions import ValidationError



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    datetime = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    hash = models.CharField(max_length=32, default=None, null=True)
    txId = models.CharField(max_length=66, default=None, null=True)

    def clean(self):
        forbidden_word = ['hack']
        for object in self.content.split():
            if object in forbidden_word:
                raise ValidationError("You're trying to write a post with a forbidden word")


    def writeOnChain(self):
        while(1):
            now = datetime.auto_now
            minutes = 10
            seconds = 60 * minutes
            time.sleep(seconds)
            self.hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
            self.txId = sendTransaction(self.hash)
            self.save()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ipAddress = models.CharField(max_length=30)
    username = models.CharField(max_length=30, default=None, null=True)

    def __str__(self):
        return self.user.username
