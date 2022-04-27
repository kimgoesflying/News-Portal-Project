from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import NewsFilter
from .forms import NewsPostForm
# Create your views here.


class NewsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 5


class NewsPostDetail(DetailView):
    model = Post
    template_name = 'news_post_detail.html'
    context_object_name = 'news_post'


class NewsSearch(NewsList):
    template_name = 'news_search.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(
            self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return NewsFilter(self.request.GET, queryset=queryset).qs


class NewsPostCreateView(CreateView):
    template_name = 'news_post_create.html'
    form_class = NewsPostForm


class NewsPostUpdateView(UpdateView):
    template_name = 'news_post_update.html'
    form_class = NewsPostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsPostDeleteView(DeleteView):
    template_name = 'news_post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
