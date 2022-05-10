from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post, Author, Category
from .filters import NewsFilter
from .forms import NewsPostForm

from django.shortcuts import render
# Create your views here.


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        Author.objects.create(username=user)
        authors_group.user_set.add(user)

    return redirect('/news')


class NewsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(
            name='authors').exists()
        return context


class NewsPostDetail(DetailView):
    model = Post
    template_name = 'news/news_post_detail.html'
    context_object_name = 'news_post'


class NewsSearch(NewsList):
    template_name = 'news/news_search.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(
            self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return NewsFilter(self.request.GET, queryset=queryset).qs


class NewsPostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news/news_post_create.html'
    form_class = NewsPostForm
    permission_required = ('news.add_post')


class NewsPostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'news/news_post_update.html'
    form_class = NewsPostForm
    permission_required = ('news.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsPostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'news/news_post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class CategoryNewsListView(NewsList):
    model = Post
    template_name = 'news/category_news_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, name=self.kwargs['category'])
        queryset = Post.objects.filter(
            category__name=self.category).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryNewsListView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context
