from django.forms import ModelForm
from .models import Post


class NewsPostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['author', 'title',  'text', ]
