from django.urls import path
from .views import *

urlpatterns = [
    path('',cart,name="cart"),
    path('remove-item/<id>',remove_item,name="remove_item"),
    path('add-item/<product_id>',add_item,name="add_item"),
]
