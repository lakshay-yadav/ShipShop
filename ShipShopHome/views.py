from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utils.email_utils import send_email_async
from .models import Query
from decouple import config


# Create your views here.
def home(request):
    return render(request,"home.html")


def policy(request):
    return render(request,"policy.html")


def about(request):
    return render(request,"about.html")


@login_required(login_url="/auth/login")
def contact_us(request):
    if request.method == "POST":
        try:
            data = request.POST

            user = request.user
            title = data.get('title')
            description = data.get('message')

            query = Query.objects.create(
                user = user,
                title = title,
                description = description
            )

            send_email_async(
                subject='Thanks for contacting ShipShop team',
                message=f'Hi {user.first_name},\nHope you are doing well. We have recieved your query.\nTitle: {title}\Description: {description}\nThanks for choosing us. Have a nice day.',
                from_email= config("MY_EMAIL"),
                recipient_list=[user.email],
            )

            messages.info(request,"Query raised successfully")
            return redirect("/")

        except Exception as e:
            print(e)
            messages.info(request,"Something wrong happened. Please try again")
            return redirect("/contact-us")

    return render(request,"contact_us.html")
