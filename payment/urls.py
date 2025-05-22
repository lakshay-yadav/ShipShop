from django.urls import path
from .views import *


urlpatterns = [
    path('donate',donate,name="donate"),
    path('failed',payment_failed,name="payment_failed"),
    path('success',payment_success,name="payment_success"),
]