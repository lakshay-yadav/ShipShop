from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from Authentication.models import CustomUser as User
from ShipShopHome.models import Query,Category,Product
from utils.email_utils import send_email_async
from django.contrib import messages
from django.db.models import Q
from payment.models import Donation


def is_admin(user):
    return user.is_authenticated and user.isAdmin


@user_passes_test(is_admin)
@login_required(login_url="/auth/login")
def admin_portal(request):
    email = request.GET.get('q')
    
    user = request.user

    if email:
        allUsers = User.objects.filter(Q(email__icontains  = email))
        allQuery = Query.objects.filter(Q(user__email__icontains  = email))
        allDonations = Donation.objects.filter(Q(user__email__icontains  = email))
    else:
        allUsers = User.objects.all()[:10]
        allQuery = Query.objects.all()[:10]
        allDonations = Donation.objects.all()[:10]

    context = {
        "user" : user,
        "allUsers" : allUsers,
        "allQuery" : allQuery,
        "allDonations" : allDonations,
        "email" : email
    }

    return render(request,"admin_portal.html",context)


@user_passes_test(is_admin)
@login_required(login_url="/auth/login")
def all_users(request):
    email = request.GET.get('q')
    user = request.user

    if email:
        allUsers = User.objects.filter(Q(email__icontains = email))
    else:
        allUsers = User.objects.all()

    context = {
        "user" : user,
        "allUsers" : allUsers,
        "email" : email
    }

    return render(request,"all_users.html",context)


@user_passes_test(is_admin)
@login_required(login_url="/auth/login")
def all_query(request):
    email = request.GET.get('q')
    user = request.user

    if email:
        allQuery = Query.objects.filter(Q(user__email__icontains = email))
    else:
        allQuery = Query.objects.all()

    context = {
        "user" : user,
        "allQuery" : allQuery,
        "email" : email
    }

    return render(request,"all_query.html",context)


@user_passes_test(is_admin)
@login_required(login_url="/auth/login")
def all_donations(request):
    email = request.GET.get('q')
    user = request.user

    sort_by = request.GET.get('sort_by', 'created_at')
    if sort_by not in ['created_at', '-created_at','amount','-amount']:
        sort_by = 'created_at'

    if email:
        allDonations = Donation.objects.filter(Q(user__email__icontains  = email)).order_by(sort_by)
    
    else:
        allDonations = Donation.objects.all().order_by(sort_by)

    context = {
        "user" : user,
        "allDonations" : allDonations,
        "email" : email,
        'sort_by': sort_by,
    }

    return render(request,"all_donations.html",context)


@user_passes_test(is_admin)
@login_required(login_url="/auth/login")
def update_query(request,id):
    query = Query.objects.get(id =id)
    context = {
        "query" : query,
    }

    if request.method == "POST":
        data = request.POST
        status = data.get('status')
        remarks = data.get('remarks')

        query.status = status
        query.remarks = remarks

        query.save()

        send_email_async(
            subject=f'Your query with title "{query.title} is now {query.status}"',
            message=f'Hi {query.user.first_name},\nYour query with title {query.title} is updated.\nThanks for connecting with us.',
            from_email= "",
            recipient_list=[query.user.email],
        )

        messages.info(request,"Query Successfully updated.")
        return redirect(f"/admin-portal/update-query/{query.id}")

    return render(request,"update_query.html",context)


@user_passes_test(is_admin)
@login_required(login_url="/auth/login")
def admin_delete_account(request,id):
    user = User.objects.get(id=id)
    user.delete()

    send_email_async(
        subject='Account deleted by Admin on ShipShop App',
        message=f'Hi {user.first_name},\nYour account is deleted by our Admin.\nPlease sign up again if you need us.\nThanks for connecting with us.',
        from_email= "",
        recipient_list=[user.email],
    )
    next_url = request.GET.get('next', '/admin-portal/all-users')

    return redirect(next_url)


@user_passes_test(is_admin)
@login_required(login_url="/auth/login")
def admin_deactivate_account(request,id):
    user = User.objects.get(id=id)
    user.isActive = False

    send_email_async(
        subject='Account deactivated by Admin on ShipShop App',
        message=f'Hi {user.first_name},\nYour account is deactivated by our Admin.\nPlease sign up again if you need us.\nThanks for connecting with us.',
        from_email= "",
        recipient_list=[user.email],
    )
    next_url = request.GET.get('next', '/admin-portal/all-users')

    return redirect(next_url)


@user_passes_test(is_admin)
@login_required(login_url="/auth/login")
def admin_product(request):

    allCategory = Category.objects.all()[:10]
    allProducts = Product.objects.all()[:10]

    context = {
        "user" : request.user,
        "allCategory" : allCategory,
        "allProducts" : allProducts
    }

    return render(request,"admin_product.html",context)


@user_passes_test(is_admin)
@login_required(login_url="/auth/login")
def all_category(request):
    category = request.GET.get('q')

    if category:
        allCategory = Category.objects.filter( name__icontains = category)
    
    else:
        allCategory = Category.objects.all()

    context = {
        "user" : request.user,
        "allCategory" : allCategory,
        "category" : category,
    }

    return render(request,"all_category.html",context)


@user_passes_test(is_admin)
@login_required(login_url="/auth/login")
def delete_category(request,id):
    category = Category.objects.get(id = id)
    category.delete()

    next_url = request.GET.get('next', '/admin-portal/product/product-category')
    messages.info(request,"Category and product from the cateogry are successfully deleted.")
    return redirect(next_url)


@user_passes_test(is_admin)
@login_required(login_url="/auth/login")
def add_category(request):
    if request.method == "POST":
        data = request.POST
        name = data.get('name')
        description = data.get('description')

        Category.objects.create(
            name = name,
            description = description
        )

        messages.info(request,"Category added successfully")
        return redirect("/admin-portal/product/product-category")

    return render(request,"add_category.html")


@user_passes_test(is_admin)
@login_required(login_url="/auth/login")
def all_product(request):
    product = request.GET.get('q')

    if product:
        allProducts = Product.objects.filter(name__icontains = product)

    else:
        allProducts = Product.objects.all()

    context = {
        "user" : request.user,
        "allProducts" : allProducts,
        "product" : product,
    }
    return render(request,"all_product.html",context)


@user_passes_test(is_admin)
@login_required(login_url="/auth/login")
def add_product(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        discount = request.POST.get('discount', 0)
        stock = request.POST.get('stock')
        new = request.POST.get('new') == 'on'

        is_available = stock !=0

        try:
            category = Category.objects.get(id=category_id)
            Product.objects.create(
                category=category,
                name=name,
                description=description,
                price=price,
                discount=discount,
                stock=stock,
                new=new,
                is_available = is_available
            )
            return redirect('/admin-portal/product/all-product')
        
        except Category.DoesNotExist:
            return render(request, 'add_product.html', {
                'categories': Category.objects.all(),
                'error': 'Invalid category selected.'
            })
        
    categories = Category.objects.all() 
    return render(request,"add_product.html",{'categories': categories})


@user_passes_test(is_admin)
@login_required(login_url="/auth/login")
def delete_product(request,id):
    next_url = request.GET.get('next','/admin-portal/product/all-product')
    product = Product.objects.get(id = id)
    product.delete()

    messages.info(request,"Product deleted")
    return redirect(next_url)


@user_passes_test(is_admin)
@login_required(login_url="/auth/login")
def edit_product(request,id):
    categories = Category.objects.all() 
    next_url = request.GET.get('next','/admin-portal/product/all-product')
    product = Product.objects.get(id = id)

    if request.method == "POST":
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        discount = request.POST.get('discount', 0)
        stock = request.POST.get('stock')
        new = request.POST.get('new') == 'on'


        try:
            category = Category.objects.get(id=category_id)
            
            product.category = category
            product.name = name
            product.description = description
            product.price = price
            product.discount = discount
            product.stock = stock
            product.new = new

            return redirect(next_url)
        
        except Category.DoesNotExist:
            return render(request, 'add_product.html', {
                'categories': Category.objects.all(),
                'error': 'Invalid category selected.'
            })


    return render(request,"edit_product.html",{'product':product,'categories':categories})

