from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import search

urlpatterns = [
    path('', views.home, name='home'),
    path('postlist/', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
    path('profile/<str:username>/follow/', views.follow_unfollow, name='follow_unfollow'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
]