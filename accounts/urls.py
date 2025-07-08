from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import profile_view, edit_profile, CustomPasswordChangeView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('verify/<str:token>/', views.verify_account, name='verify_account'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]