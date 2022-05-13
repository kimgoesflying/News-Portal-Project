from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Post, Author, Category, Subscriber
from .filters import NewsFilter
from .forms import NewsPostForm


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        Author.objects.create(username=user)
        authors_group.user_set.add(user)

    return redirect('/news')


@login_required
def subscribe(request, category):
    user_mail = request.user.email
    cat = Category.objects.get(name=category)

    if not cat.subscriber.filter(mail=user_mail).exists():
        if Subscriber.objects.filter(mail=user_mail).exists():
            sub = Subscriber.objects.get(mail=user_mail)
        else:
            sub = Subscriber.objects.create(mail=user_mail)
        cat.subscriber.add(sub)
        message = 'Вы успешно подписались на рассылку новостей категории'
    else:
        message = 'Вы уже подписаны на категорию'
    return render(request, 'news/subscribe.html',
                  {'category': category, 'message': message})


class NewsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        category_menu = Category.objects.all()
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(
            name='authors').exists()
        context['category_menu'] = category_menu
        return context


class NewsPostDetail(DetailView):
    model = Post
    template_name = 'news/news_post_detail.html'
    context_object_name = 'news_post'

    def get_context_data(self, **kwargs):
        category_menu = Category.objects.all()
        context = super().get_context_data(**kwargs)
        context['category_menu'] = category_menu
        return context


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
    success_url = '/news'

    def form_valid(self, form):
        response = super().form_valid(form)
        form.send(self.object.pk)
        return response

    def get_context_data(self, **kwargs):
        category_menu = Category.objects.all()
        context = super().get_context_data(**kwargs)
        context['category_menu'] = category_menu
        return context


class NewsPostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'news/news_post_update.html'
    form_class = NewsPostForm
    permission_required = ('news.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        category_menu = Category.objects.all()
        context = super().get_context_data(**kwargs)
        context['category_menu'] = category_menu
        return context


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
