from django.urls import path
from .views import *


urlpatterns = [
    path('',admin_portal,name="admin_portal"),
    path('all-users',all_users,name="all_users"),
    path('all-query',all_query,name="all_query"),
    path('update-query/<id>',update_query,name="update_query"),
    path('all-donations',all_donations,name="all_donations"),
    path('delete_account/<id>',admin_delete_account,name="admin_delete_account"),
    path('deactivate_account/<id>',admin_deactivate_account,name="admin_deactivate_account"),

    path('product',admin_product,name="admin_product"),

    path('product/product-category',all_category,name="all_category"),
    path('product/delete-category/<id>',delete_category,name="delete_category"),
    path('product/add-category',add_category,name="add_category"),

    path('product/all-product',all_product,name="all_product"),
    path('product/add-product',add_product,name="add_product"),
    path('product/delete-product/<id>',delete_product,name="delete_product"),
    path('product/edit-product/<id>',edit_product,name="edit_product"),

]