from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Cart.models import CartItem
from ShipShopHome.models import Product
from .models import Order,OrderProduct,Payment
from UserProfile.models import Address,STATE_CHOICES
from utils.payment_session import *


# Create your views here.
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    user_addresses = Address.objects.filter(user = request.user)
    total_price = 0
    quantity = 0

    for cart_item in cart_items:
        total_price += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    grand_total = total_price
    handing = 15.00
    total = float(grand_total) + handing
    
    context = {
        'total_price': total_price,
        'quantity': quantity,
        'cart_items':cart_items,
        'handing': handing,
        'order_total': total,
        "user_addresses" : user_addresses,
        'STATE_CHOICES': STATE_CHOICES
    }

    if request.method == "POST":
        form_type = request.POST.get('form_type')
        if form_type == "add_address":
            Address.objects.create(
                user=request.user,
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                address_line1=request.POST['address_line1'],
                address_line2=request.POST.get('address_line2', ''),
                landmark=request.POST.get('landmark', ''),
                city=request.POST['city'],
                state=request.POST['state'],
                pincode=request.POST['pincode']
            )
            messages.info(request,"Successfully added address.")
            return redirect("/orders/checkout")
        
        elif form_type=="order":
            data = request.POST
            selected_address = data.get('selected_address')
            selected_address = Address.objects.get(id = selected_address)

            order = Order.objects.create(
                order_total = total,
                user = request.user,
                address = selected_address,
                order_number = ""
            )

            order.order_number = order.id
            order.save()
            print(order)
            print(order.id)

            for cart_item in cart_items:
                OrderProduct.objects.create(
                    order = order,
                    user = request.user,
                    product = cart_item.product,
                    quantity = cart_item.quantity,
                    product_price = cart_item.product.price,
                )
            
            purpose = "order"
            amount = int(total)
            email = request.user.email

            try:
                checkout_session = payment_session_create(request,amount,purpose,email,order.id)
            
            except Exception as e:
                print(e)
                messages.info(request,"Error Occurred. Please try again")
                return redirect("")
            
            print(checkout_session)
            return redirect(checkout_session.url)
            
    return render(request,"checkout.html",context)
