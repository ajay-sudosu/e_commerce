from django.contrib.auth import views as auth_views
from django.urls import path

from account.forms import UserLoginForm
from account.views import *

app_name = 'account'

urlpatterns = [
    path('register/', account_register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html',
                                                form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),
    # user dashboard
    path('dashboard/', dashboard, name='dashboard'),
    path('activate/<slug:uidb64>/<slug:token>/', account_activate, name='activate'), ]
