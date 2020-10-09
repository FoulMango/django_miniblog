from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
import datetime


class BlogPost(models.Model):
    title = models.CharField(max_length=30, default=f'Blog posted on {datetime.date.today()}')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    txt = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['creation_date']


class Comment(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    txt = models.TextField()

    def __str__(self):
        return f'Comment by {self.author} on {self.creation_date.ctime()}'

    class Meta:
        ordering = ['creation_date']


class Biography(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
