from email.policy import default
from django.db import models
from django.conf import settings
from django.utils import timezone


class User(models.Model):
    email= models.EmailField()
    password=models.CharField(max_length=16)


class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    save_date = models.DateTimeField(blank=True, null=True)
    tags=models.CharField(max_length=200, null=True)

    '''def addtag(self):
        self.tags.append(models.CharField(max_length=40))'''

    def savetoapp(self):
        self.save_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
# Create your models here.
