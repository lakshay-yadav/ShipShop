from django.shortcuts import render,redirect
from .models import CustomUser as User,PasswordResetOTP
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import random
from decouple import config
import stripe
from utils.email_utils import send_email_async

# Create your views here.
def register(request):
    if request.method =="POST":
        user_data = request.POST

        first_name = user_data.get('first_name').strip()
        last_name = user_data.get('last_name').strip()
        password = user_data.get('password').strip()
        confirm_password = user_data.get('confirm_password').strip()
        email = user_data.get('email').strip()

        user = User.objects.filter(email = email)

        if user.exists():
            messages.info(request,"Account already exists")
            return redirect("/auth/register")

        if password != confirm_password or len(password)<6:
            messages.info(request,"Password does not macth or Password length less than 6.")
            return redirect("/auth/register")

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
        )

        user.set_password(password)

        user.save()

        send_email_async(
            subject='Registration Successfully at ShipShop',
            message=f'Hi {user.first_name},\nYou have successfully registered at ShipShop Application.\nThanks for joining us.\nTeam ShipShop.',
            from_email= config("MY_EMAIL"),
            recipient_list=[user.email],
        )

        messages.info(request,"User successfully registered")

        return redirect("/auth/login")

    return render(request,"register.html")


def login_page(request):
    if request.method =="POST":
        user_data = request.POST

        password = user_data.get('password').strip()
        email = user_data.get('email').strip()

        user = authenticate(email = email,password = password)

        if not user:
            messages.error(request,"Invalid email or password")
            return redirect("/auth/login")
        
        if not user.isActive :
            messages.error(request,"Your account is deactivated.Please activate your account.")
            return redirect("/auth/activate-account")

        login(request,user)
        return redirect("/")

    return render(request,"login.html")


def logout_page(request):
    logout(request)
    return redirect("/")


def forget_password(request):
    if request.method == "POST":
        data = request.POST
        email = data.get('email')

        user = User.objects.filter(email = email)

        if not user:
            messages.info(request,"User does not exists.Please register yourself.")
            return redirect("/auth/forget-password")
        
        else:
            try:
                user = user[0]
                user_id = user.id
                print(user_id)

                first_name = user.first_name

                otp = str(random.randint(100000, 999999))
                print("OTP ->",otp)

                PasswordResetOTP.objects.create(user=user, otp=otp)

                send_mail(
                    subject='ShipShop OTP for Password Reset',
                    message=f'Hi {first_name},\nYour OTP to reset the password on ShipShop app : {otp}.\nPlease use this otp to reset your password.It will be valid for only 15 mins\nThanks for choosing us.\nTeam ShipShop.',
                    from_email= config("MY_EMAIL"),
                    recipient_list=[email],
                )

                return redirect(f"/auth/forget-password/{user_id}")
            
            except Exception as e:
                print(e)
                messages.info(request,"Some error occured! Please try again")
                return render(request,"forget_password.html")       

    return render(request,"forget_password.html")


def forget_password_authenticate(request,id):
    if request.method == "POST":
        data = request.POST
        otp = data.get('otp')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        user = User.objects.get(id = id)
        user = user

        if not PasswordResetOTP.objects.filter(user = user).exists():
            messages.info(request,"Did not able to get the OTP. Kindly start from the beginning.")
            return redirect("/auth/forget-password")
        
        original_otp = PasswordResetOTP.objects.filter(user = user)

        original_otp = original_otp[0]


        otp_from_db = int(original_otp.otp)
        otp = int(otp)

        if original_otp.is_expired():
            original_otp.delete()  
            messages.info(request,"Expired OTP. Please try again")
            return render(request,"forget_password_authenticate.html")

        if otp_from_db != otp:
            messages.info(request,"Wrong OTP. Please try again")
            return render(request,"forget_password_authenticate.html")
        
        if password != confirm_password:
            messages.error(request,"Password and confirm password does not match")
            return render(request,"forget_password_authenticate.html")

        user.set_password(password)
        user.save()

        send_email_async(
            subject='Password Change Alert',
            message=f'Hi {user.first_name},\nYou have changed your password recently.\nTeam ShipShop.',
            from_email= config("MY_EMAIL"),
            recipient_list=[user.email],
        )

        original_otp.delete()

        messages.info(request,"Password reset done. Please login")
        return redirect("/auth/login")

    return render(request,"forget_password_authenticate.html")


def activate_account(request):
    otp_sent = False
    email = ""

    if request.POST:
        form_type = request.POST.get('form_type')

        if form_type == "request_otp":
            email = request.POST.get('email')

            user = User.objects.filter(email= email)
            if not user:
                messages.info(request,"Account does not exists.Please register yourself.")
                return redirect("/auth/register")
            
            user = user[0]
            if user.isActive:
                messages.info(request,"Your account is already Active. Please login.")
                return redirect("/auth/login")
            
            first_name = user.first_name

            otp = str(random.randint(100000, 999999))
            print("OTP ->",otp)

            PasswordResetOTP.objects.create(user=user, otp=otp)

            send_mail(
                subject='ShipShop OTP for Account activation',
                message=f'Hi {first_name},\nYour OTP to Activate your account on ShipShop app : {otp}.\nPlease use this otp to activate your account. It will be valid for only 15 mins\nThanks for choosing us.\nTeam ShipShop.',
                from_email= config("MY_EMAIL"),
                recipient_list=[email],
            )

            request.session['otp_email'] = email 
            
            otp_sent = True


        elif form_type == "verify_otp":
            otp = request.POST.get('otp')
            email = request.session['otp_email']
            
            user = User.objects.filter(email = email)[0]
            # print(user)

            if not PasswordResetOTP.objects.filter(user = user).exists():
                messages.info(request,"Did not able to get the OTP. Kindly start from the beginning.")
                return redirect("/auth/activate-account")

            original_otp = PasswordResetOTP.objects.filter(user = user)[0]

            otp_from_db = int(original_otp.otp)
            otp = int(otp)

            if original_otp.is_expired():
                original_otp.delete()  
                messages.info(request,"Expired OTP. Please try again")
                return render(request,"acivate_account.html")

            if otp_from_db != otp:
                messages.info(request,"Wrong OTP. Please try again")
                return render(request,"acivate_account.html")

            user.isActive = True
            user.save()

            send_email_async(
                subject='ShipShop - Account successfully activated',
                message=f'Hi {user.first_name},\nYou account is successfully activated.\nTeam ShipShop.',
                from_email= config("MY_EMAIL"),
                recipient_list=[user.email],
            )

            original_otp.delete()
            request.session.pop('otp_email', None)

            messages.info(request,"Account successfully activated. Please login")
            return redirect("/auth/login")

    return render(request,"activate_account.html",{"otp_sent":otp_sent,"email":email})
