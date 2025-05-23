from django.shortcuts import render,redirect
from Authentication.models import CustomUser as User,PasswordResetOTP
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from utils.email_utils import send_email_async
from utils.payment_session import *
from .models import Donation
from Order.models import Payment,Order,OrderProduct
from Cart.models import CartItem

# Create your views here.
@login_required(login_url="/auth/login")
def donate(request):
    if request.method == "POST":
        try:
            data = request.POST
            amount = data.get('amount')
            email = request.user.email

            if not amount:
                messages.info(request,"Please enter amount .")
                return redirect("/payment/donate")
            
            purpose = "Donation"
            amount = int(amount)
            
            checkout_session = payment_session_create(request,amount,purpose,email)
        
        except Exception as e:
            print(e)
            messages.info(request,"Error Occurred. Please try again")
            return redirect("/payment/donate")
        
        return redirect(checkout_session.url)

    return render(request,"donate.html")


@login_required(login_url="/auth/login")
def payment_failed(request):
    purpose = request.GET.get('purpose')

    if purpose == "Donation":
        messages.info(request,"Payment Error. Please try again.")
        return redirect("/payment/donate")

    elif purpose == 'order':
        order_id = request.GET.get('order_id')
        messages.info(request,"Payment failed.Please try again")
        return redirect("/cart")
    
    else:
        return redirect("/")


@login_required(login_url="/auth/login")
def payment_success(request):
    session_id = request.GET.get('session_id')
    purpose = request.GET.get('purpose')
    user = request.user
    session = stripe.checkout.Session.retrieve(session_id)
    email = session.get("customer_email")
    amount = session.get("amount_total")

    if purpose == "Donation":
        Donation.objects.create(
            amount = amount/100,
            user =  user
        )
        messages.info(request,"Payment successfully done. Thanks for your contribution.")
    
    elif purpose == "order":
        order_id = request.GET.get('order_id')
        order = Order.objects.get(id = order_id)
        order.is_ordered = True
        order.save()

        cart_items = CartItem.objects.filter(user = request.user)
        cart_items.delete()

        messages.info(request,"Order placed successfully.")
        
    return redirect("/")
