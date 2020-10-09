from django.urls import path, include
from . import views

app_name = 'blog'

blogpost_patterns = [
    path('', views.BlogDetailView.as_view(), name='blog-detail'),
    path('add-comment/', views.add_comment_view, name='add-comment'),
    path('update/', views.BlogPostUpdate.as_view(), name='blogpost-update'),
]

urlpatterns = [
    path('', views.BlogView.as_view(), name='blog-index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blogger/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('add/', views.BlogPostCreate.as_view(), name='blogpost-add'),
    path('<int:pk>/', include(blogpost_patterns)),
]
