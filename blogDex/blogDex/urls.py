"""blogDex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('admin/', admin.site.urls),
    path ('', views.posts),
    path ('posts', views.posts),
    path ('newPost', views.newPost, name='newPost'),
    path ('register', views.register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='blog/login.html', redirect_field_name='login'),  name='login'),
    path('newPost/posting', views.posting, name='posting'),
    path ('counter', views.counter, name='counter'),
    path('user/<str:pk>/', views.id_user, name = 'user'),
    path('lastPosts', views.lastPosts),
    path ('wordCheck', views.wordCheck),


]