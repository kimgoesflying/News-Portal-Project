from django.urls import path
from .views import NewsList, NewsPostDetail, NewsPostCreateView, NewsPostUpdateView, NewsPostDeleteView


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsPostDetail.as_view(), name='news_post'),
    path('add/', NewsPostCreateView.as_view(),
         name='news_post_create'),
    path('<int:pk>/edit', NewsPostUpdateView.as_view(), name='news_post_update'),
    path('<int:pk>/delete', NewsPostDeleteView.as_view(), name='news_post_delete'),
]
