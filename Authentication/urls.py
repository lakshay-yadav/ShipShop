from django.urls import path
from .views import *


urlpatterns = [
    path('register',register,name="register"),
    path('login',login_page,name="login_page"),
    path('logout',logout_page,name="logout_page"),
    path("forget-password", forget_password, name="forget_password"),
    path("forget-password/<id>",forget_password_authenticate,name="forget_password_authenticate"),
    path("activate-account",activate_account,name="activate_account"),
]