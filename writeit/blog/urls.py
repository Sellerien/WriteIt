from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.BlogHome.as_view(), name="home"),
    path('post/<int:pk>/', views.ShowPost.as_view(), name="post_detail"),
    path('addpost/', views.AddPost.as_view(), name="add_post"),
    path('category/<slug:cat_slug>/', views.CategoryView.as_view(), name='category'),
    path('post/myposts/', views.MyPosts.as_view(), name='my_posts'),
    path('search/', views.ArticleSearchView.as_view(), name='search'),
    path('edit/<int:pk>/', views.UpdatePost.as_view(), name='edit_post'),
    path('delete/<int:pk>/', views.DeletePost.as_view(), name='delete_post'),
    path('delete_comment/<int:pk>/', views.DeleteComment.as_view(), name='delete_comment'),
    ]