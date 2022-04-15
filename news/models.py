from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Author(models.Model):
    username = models.OneToOneField(
        User, on_delete=models.CASCADE)
    raiting = models.IntegerField(default=0)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article = 'AR'
    news = 'NW'

    POST_TYPE = [
        (article, 'статья'),
        (news, 'новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(
        max_length=2, choices=POST_TYPE, default=article)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    category = models.ManyToManyField(
        Category, through='PostCategory', blank=True)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
