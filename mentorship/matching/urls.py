from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('register/', views.register, name='register'),
    path('users/<int:user_id>', views.userPage, name='userPage'),
    path('test/', views.testPage, name='testPage'),
    path('update/', views.userUpdate, name='userUpdate'),
    path('register/update/', views.userUpdate, name='userUpdate'),
]
