from celery import shared_task
# import time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Post, Subscriber


@shared_task
def send_newspost_createed_mail_task(id):
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
