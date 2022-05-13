
from django import forms
from .models import Post, Subscriber
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User


class NewsPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('author', 'category', 'title',  'text')

        widgets = {
            'author': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }

        labels = {
            'author': ('Автор'),
            'category': ('Категория'),
            'title': ('Заголовок'),
            'text': ('Текст'),
        }

    def get_info(self):
        cl_data = super().clean()

        text = cl_data.get('text')
        title = cl_data.get('title')
        categories = cl_data.get('category')

        return text, title, categories

    def send(self, pk):
        text, title, categories = self.get_info()
        subs = Subscriber.objects.filter(category__in=categories)
        if subs:
            for sub in subs:
                username = User.objects.get(email=sub)
                html_content = render_to_string(
                    'news/news_post_created.html',
                    {
                        'text': text,
                        'title': title,
                        'username': username,
                        'url': f'http://127.0.0.1:8000/news/{pk}'
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=title,
                    body=text,
                    from_email='peterbadson@yandex.ru',
                    to=[sub],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
