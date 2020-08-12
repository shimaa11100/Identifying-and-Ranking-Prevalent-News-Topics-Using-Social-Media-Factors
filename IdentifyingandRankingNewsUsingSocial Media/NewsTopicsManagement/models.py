from django.db import models
from UserDataManagement.models import Topic, User


# NewsTopicsManagement models here.


class Article(models.Model):
    ArticleDescription = models.CharField(max_length=1000)
    TopicNameFK = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.ArticleDescription


class History(models.Model):
    SearchTitle = models.CharField(max_length=200)
    UserEmailFK = models.ForeignKey(User, on_delete=models.CASCADE)
    Date_Time = models.CharField(max_length=100)

    def __str__(self):
        return self.SearchTitle + ' - ' + 'Data&time ' + self.Date_Time


class Feedback(models.Model):
    FeedbackTitle = models.CharField(max_length=200)
    UserEmailFK = models.ForeignKey(User, on_delete=models.CASCADE)
    ArticleFK = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.FeedbackTitle
