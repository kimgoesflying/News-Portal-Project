from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
# Create your models here.


class Author(models.Model):
    username = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = Post.objects.filter(author_id=self.pk).aggregate(
            Sum('rating'))['rating__sum'] * 3

        comment_rating = Comment.objects.filter(
            username_id=self.username).aggregate(Sum('rating'))['rating__sum']

        post_comment_rating = Comment.objects.filter(
            post__author=self.pk).aggregate(Sum('rating'))['rating__sum']

        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()

    def __str__(self):
        return self.username.username.title()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name.title()


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

    def preview(self):
        preview = f'{self.text[0:124]} ...'
        return preview

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()

    def __str__(self):
        return f'{self.pk} {self.title.title()}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.post.title.title()}  {self.category.name.title()}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()

    def preview(self):
        preview = f'{self.text[0:124]} ...'
        return preview

    def __str__(self):
        return self.preview().title()
