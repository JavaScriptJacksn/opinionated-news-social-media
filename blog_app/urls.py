"""opinionated_news URL Configuration

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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name="home"),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('poll/<slug:slug>', views.PostPoll.as_view(), name='post_poll'),
    path('blog_app/create_post/', views.CreatePost.as_view(), name='create_post'),
    path('blog_app/create_poll/<slug:slug>', views.CreatePoll.as_view(), name='create_poll'),
    path('blog_app/edit_post/<slug:slug>', views.EditPost.as_view(), name='edit_post'),
    path('blog_app/edit_poll/<slug:slug>', views.EditPoll.as_view(), name='edit_poll'),
    path('blog_app/profile/', views.Profile.as_view(), name='profile'),
]
