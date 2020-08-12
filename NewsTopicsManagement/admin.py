from django.contrib import admin
from .models import Article, History, Feedback
# Register your models here.

admin.site.register(Article)
admin.site.register(History)
admin.site.register(Feedback)
