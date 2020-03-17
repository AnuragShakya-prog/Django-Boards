from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from markdown import markdown
from django.utils.html import mark_safe
# Create your models here.


class Board(models.Model):
    name=models.CharField(max_length=40,unique=True)
    description=models.TextField(max_length=500)
    

    def get_post_count(self):
        return Post.objects.filter(topic__board=self).count()
    
    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject=models.CharField(max_length=250)
    last_updated=models.DateTimeField(auto_now_add=True)
    board=models.ForeignKey(Board,related_name="topics",on_delete=models.CASCADE)
    starter=models.ForeignKey(User,related_name="topics",on_delete=models.CASCADE)
    views=models.ManyToManyField(User,related_name='+')


    
    def get_views_count(self):
        return self.views.all().count()

class Post(models.Model):
    message=models.TextField(max_length=4000)
    topic=models.ForeignKey(Topic,related_name="posts",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True)
    created_by=models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    updated_by=models.ForeignKey(User,related_name='+',null=True,on_delete=models.SET_NULL)



    def get_absolute_url(self):
        return reverse('topic_posts',args=[self.topic.board.pk,self.topic.pk])



    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message,safe_mode='escape'))