from django.urls import path
from .views import *

urlpatterns = [
    path('',cart,name="cart"),
    path('remove-item/<id>',remove_item,name="remove_item"),
]
