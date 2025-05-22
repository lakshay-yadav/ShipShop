from django.shortcuts import render,redirect
from Authentication.models import CustomUser as User
from payment.models import Donation
from ShipShopHome.models import Query
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from decouple import config
from utils.email_utils import send_email_async


@login_required(login_url="/auth/login")
def profile(request):
    return render(request,"profile.html")


@login_required(login_url="/auth/login")
def change_password(request):
    if request.method == "POST":
        data = request.POST
        password = data.get('password')
        new_password = data.get('new_password').strip()
        confirm_password = data.get('confirm_password').strip()
        user = request.user

        isCorrectPassword = user.check_password(password)
        if not isCorrectPassword:
            messages.info(request,"Incorrect password")
            return redirect("/profile/change-password")
        
        if not new_password:
            messages.info(request,"Please add new password")
            return redirect("/profile/change-password")
        
        if new_password != confirm_password  or len(password)<6:
            messages.info(request,"New password and Confirm Password does not match! or Password length is less than 6")
            return redirect("/profile/change-password")
        
        user.set_password(new_password)
        user.save()

        send_email_async(
            subject='Password reset on To-Do app',
            message=f'Hi {user.first_name},\nYou have successfully changed your password.\nThanks for choosing us',
            from_email= config("MY_EMAIL"),
            recipient_list=[user.email],
        )

        login(request,user)

        messages.info(request,"Password successfully changed. Please login again.")
        return redirect("/profile")


    return render(request,"change_password.html")


@login_required(login_url="/auth/login")
def orders(request):
    return render(request,"orders.html")


@login_required(login_url="/auth/login")
def wishlist(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user = user)
    return render(request,"wishlist.html",{'wishlist_items': wishlist_items})


@login_required(login_url="/auth/login")
def add_to_wishlist(request,product_id):
    user = request.user
    isAdded = Wishlist.objects.filter(user=user,product__id = product_id)
    if isAdded:
        messages.info(request,"Already in wishlist")
        return redirect(f"/product-details/{product_id}")
    
    product = Product.objects.get(id = product_id)

    Wishlist.objects.create(
        user = user,
        product = product
    )

    messages.info(request,"Product added to wishlist")

    return redirect(f"/product-details/{product_id}")


@login_required(login_url="/auth/login")
def delete_from_wishlist(request,product_id):
    next_url = request.GET.get('next')
    user = request.user
    wishlist_item = Wishlist.objects.filter(user = user)
    if wishlist_item:
        wishlist_item.delete()
        messages.info(request,"Item removed from Wishlist")

    return redirect(next_url)


@login_required(login_url="/auth/login")
def donations(request):
    user = request.user

    sort_by = request.GET.get('sort_by', 'created_at')
    if sort_by not in ['created_at', '-created_at','amount','-amount']:
        sort_by = 'created_at'

    donations = Donation.objects.filter(user = user).order_by(sort_by)
    context = {
        "donations" : donations,
        "sort_by" : sort_by,
    }
    return render(request,"donations.html",context)


@login_required(login_url="/auth/login")
def queries(request):
    user = request.user
    queries = Query.objects.filter(user = user)
    context = {
        "queries" : queries,
        "user" :user,
    }
    return render(request,"queries.html",context)

@login_required(login_url="/auth/login")
def query_details(request,id):
    query = Query.objects.get(id = id)
    context = {
        "query" : query
    }
    return render(request,"query_details.html",context)


@login_required(login_url="/auth/login")
def saved_address(request):
    user = request.user
    addresses = Address.objects.filter(user = user)
    context = {
        "addresses" : addresses,
        "user" : user,
    }
    return render(request,"saved_address.html",context)


@login_required(login_url="/auth/login")
def add_new_address(request):
    if request.method == "POST":
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
        return redirect('/profile/saved-address')
    
    return render(request,"add_new_address.html",{'state_choices': STATE_CHOICES})


@login_required(login_url="/auth/login")
def edit_address(request,id):
    user = request.user
    address = Address.objects.get(id = id)
    context = {
        "address" : address,
        "user" : user,
        'state_choices': STATE_CHOICES
    }

    if request.method == "POST":
        data = request.POST

        address.first_name = request.POST['first_name']
        address.last_name = request.POST['last_name']
        address.address_line1=request.POST['address_line1']
        address.address_line2=request.POST.get('address_line2', '')
        address.landmark=request.POST.get('landmark', '')
        address.city=request.POST['city']
        address.state=request.POST['state']
        address.pincode=request.POST['pincode']

        address.save()

        messages.info(request,"Address updated.")
        return redirect('/profile/saved-address')

    return render(request,"edit_address.html",context)


@login_required(login_url="/auth/login")
def update_account(request,id):
    if request.method == "POST":
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        user = request.user

        user.first_name = first_name
        user.last_name = last_name

        user.save()

        messages.info(request,"Profile updated successfully.")
        return redirect("/profile")

    return render(request,"update_account.html")


@login_required(login_url="/auth/login")
def delete_account(request,id):
    user = request.user
    user.delete()

    send_email_async(
        subject='ShipShop Account deleted',
        message=f'Hi {user.first_name},\nIt is hard to let you go. Your account and data related to it is successfully deleted.\nPlease sign up again if you need us.\n Thanks for connecting with us.',
        from_email= config("MY_EMAIL"),
        recipient_list=[user.email],
    )

    messages.info(request,"Successfully deleted account")
    return redirect("/")


@login_required(login_url="/auth/login")
def deactivate_account(request,id):
    user = request.user
    user.isActive = False
    user.save()

    logout(request)

    send_email_async(
        subject='ShipShop Account deactivated',
        message=f'Hi {user.first_name},\nIt is hard to let you go. Your account is successfully deactivated.\nPlease activate your account if you need us. We will delete any of your data.\n Thanks for connecting with us.',
        from_email= config("MY_EMAIL"),
        recipient_list=[user.email],
    )

    messages.info(request,"Successfully deactivated account")
    return redirect("/")


@login_required(login_url="/auth/login")
def reviews(request):
    return render(request,"reviews.html")
