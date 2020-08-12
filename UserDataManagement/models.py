from django.db import models


# User Data Management models here.

class User(models.Model):
    UserEmail = models.CharField(primary_key=True, max_length=100)
    UserName = models.CharField(max_length=100)
    UserPassword = models.CharField(max_length=50)

    def __str__(self):
        return self.UserEmail+' - '+self.UserName


class Topic(models.Model):
    TopicName = models.CharField(primary_key=True, max_length=100)
    TopicMembers = models.ManyToManyField(User)

    def __str__(self):
        return self.TopicName




