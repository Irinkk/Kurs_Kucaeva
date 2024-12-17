from . import views
from django.urls import path
from .views import register, CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.index),
    path('home',views.index, name='home'),
    path('register', register, name='register'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('client-dashboard', views.client_dashboard, name='client_dashboard'),
    path('moderator-dashboard', views.moderator_dashboard, name='moderator_dashboard'),
    path('create-ad', views.create_ad, name='create_ad'),  # Страница подачи объявления
    path('ad/<int:id>/', views.ad_detail, name='ad_detail'),
    path('profile/', views.user_profile, name='user_profile'),
    path('delete_ad/<int:ad_id>/', views.delete_ad, name='delete_ad'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('moderation/', views.moderation, name='moderation'),
]

