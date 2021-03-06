from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth.models import Group
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
        return self.username.username


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscriber = models.ManyToManyField(
        'Subscriber', through='CategorySubscriber')

    def __str__(self):
        return self.name


class Subscriber(models.Model):
    mail = models.EmailField(max_length=254, unique=True)

    def __str__(self):
        return self.mail


class CategorySubscriber(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(
        Subscriber, on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.category} | {self.subscriber}'


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
        Category, through='PostCategory')

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
        return f'{self.title} | {self.author}'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.post.title} | {self.category.name}'


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
        return self.preview()


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


class CommonSocialSignupForm(SocialSignupForm):

    def save(self, request):
        user = super(CommonSocialSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
