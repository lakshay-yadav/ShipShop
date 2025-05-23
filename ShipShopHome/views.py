from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utils.email_utils import send_email_async
from Authentication.models import CustomUser as User
from UserProfile.models import Wishlist
from ShipShopHome.models import Query,Category,Product
from .models import Query
from decouple import config


# Create your views here.
def home(request):
    categories = Category.objects.all()
    for category in categories:
        category.products = Product.objects.filter(category=category, stock__gt=0)
    return render(request,"home.html",{'categories': categories})


def product_details(request,product_id):
    product = Product.objects.get(id = product_id)
    related_products = Product.objects.filter(category = product.category)[:4]
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    
    
    return render(request,"product_details.html",{"product":product,"related_products":related_products,"in_wishlist":in_wishlist,})


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


def product_by_category(request,name):
    allProducts = Product.objects.filter(category__name=name)
    query = request.GET.get('q')
    if query:
        allProducts = allProducts.filter(name__icontains=query)

    context = {
        "allProducts" : allProducts,
        "category_name" : name,
        "query" : query
    }
    return render(request,"product_by_category.html",context)

