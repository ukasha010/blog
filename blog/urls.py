from django.contrib import admin
from django.urls import path
from blog import views
from .views import PostListView , PostDetailView , PostCreateView , PostUpdateView , PostDeleteView , UserPostListView
from users import views as user_views
urlpatterns = [
    path('', PostListView.as_view() , name = 'blog-home'),
    path('user/<str:username>', UserPostListView.as_view() , name = 'user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view() , name = 'post-detail'), # URL containing varaible. Django provide us ability to use variable in our urls.
    path('about/' , views.about , name = 'blog-about'),
    path('post/new/' , PostCreateView.as_view() , name = 'post-create'), #url for this view is not like other view.
    path('post/update/<int:pk>/' , PostUpdateView.as_view() , name = 'post-update'),
    path('post/delete/<int:pk>/' , PostDeleteView.as_view() , name = 'post-delete'),
    path('post/like/<int:pk>/' , views.like_post , name = 'like-post'),
    path('post/comment/<int:pk>/' , views.PostComment , name='post-comment'),
    path('user/follow/<str:author>/' , user_views.FollowUser , name='user-follow'),
    path('user/profile/<str:author>/' , user_views.UserProfile , name='user-profile'),
    #path('permission_testing/' , views.permission_testing , name="permission_testing"),
    path('notifications/' , views.notify , name='notifications')
]
