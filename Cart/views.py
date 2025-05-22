from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from Authentication.models import CustomUser as User
from ShipShopHome.models import Query,Category,Product
from .models import  CartItem
from utils.email_utils import send_email_async
from django.contrib import messages
from django.db.models import Q


# Create your views here.
@login_required(login_url="/auth/login")
def cart(request):
    total_price = 0
    quantity = 0
    user = request.user
    cart_items = CartItem.objects.filter(user = user)

    for cart_item in cart_items:
        total_price += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    context = {
        'total' : total_price,
        'quantity': quantity,
        'cart_items':cart_items,
    }

    return render(request,"cart.html",context)


@login_required(login_url="/auth/login")
def remove_item(request,id):
    cart_item = CartItem.objects.get(id = id)
    cart_item.delete()

    return redirect("/cart")


@login_required(login_url="auth/login")
def add_item(request,product_id):
    return redirect("/cart")