from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('tweet/', views.create_tweet, name='create_tweet'),
    path('tweet/<int:tweet_id>/like/', views.toggle_like, name='toggle_like'),
    path('tweet/<int:tweet_id>/delete/', views.delete_tweet, name='delete_tweet'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
