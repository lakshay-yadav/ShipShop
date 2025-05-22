from django.urls import path
from .views import *


urlpatterns = [
    path('',profile,name="profile"),

    path('change-password',change_password,name="change_password"),
    path('update-account/<id>',update_account,name="update_account"),
    path('delete-account/<id>',delete_account,name="delete_account"),
    path('deactivate-account/<id>',deactivate_account,name="deactivate_account"),

    path('orders',orders,name="orders"),

    path('wishlist',wishlist,name="wishlist"),
    path('add-to-wishlist/<product_id>',add_to_wishlist,name="add_to_wishlist"),
    path('delete-from-wishlist/<product_id>',delete_from_wishlist,name="delete_from_wishlist"),

    path('donations',donations,name="donations"),

    path('reviews',reviews,name="reviews"),
    
    path('saved-address',saved_address,name="saved_address"),
    path('add-new-address',add_new_address,name="add_new_address"),
    path('edit-address/<id>',edit_address,name="edit_address"),

    path('queries',queries,name="queries"),
    path('query/<id>',query_details,name="query_details"),
]
