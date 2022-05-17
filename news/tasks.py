from celery import shared_task
# import time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Post, Subscriber
from datetime import datetime, timedelta


@shared_task
def send_newspost_created_mail_task(id):
    post = Post.objects.get(pk=id)
    postcategories = post.category.all()
    subs = Subscriber.objects.filter(
        category__in=postcategories)

    for sub in subs:
        username = User.objects.get(email=sub)
        html_content = render_to_string(
            'news/mail_news_post_created.html',
            {
                'text': post.text,
                'title': post.title,
                'username': username,
                'url': f'http://127.0.0.1:8000/news/{id}'
            }
        )

        msg = EmailMultiAlternatives(
            subject=post.title,
            to=[sub],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print('mail sent to', sub)


@shared_task
def news_weekly_mail_task():
    one_week_ago = datetime.today() - timedelta(days=7)
    new_posts = Post.objects.filter(date__gte=one_week_ago)
    subscribers = Subscriber.objects.all()

    for sub in subscribers:
        username = User.objects.get(email=sub)
        mail_posts = new_posts.filter(category__subscriber__mail=sub)

        html_content = render_to_string(
            'news/mail_news_post_list.html',
            {
                'mail_posts': mail_posts,
                'username': username,
            }
        )

        msg = EmailMultiAlternatives(
            subject='NewsPortal weekly',
            to=[sub],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print('--------', 'mail sent to', sub)
