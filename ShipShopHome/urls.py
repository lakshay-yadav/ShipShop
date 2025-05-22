from django.urls import path
from .views import *


urlpatterns = [
    path('',home,name="home"),

    path('policy',policy,name="policy"),

    path('about',about,name="about"),

    path('contact-us',contact_us,name="contact_us"),

    path('product-details/<product_id>',product_details,name="product_details"),

    path('category/<name>',product_by_category,name="product_by_category"),
]