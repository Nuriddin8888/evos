from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout

import random

from .user_info import generate_first_name
from users.models import User, VerificationCode
from products.models import Cart

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse




# Create your views here.
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user_email = request.POST.get("user_email")
        password = request.POST.get("password")
        
        print(username, user_email, password)


        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Bu username allaqachon olingan!"})
        if user_email:
            if "@" in user_email:
                if User.objects.filter(email=user_email).exists():
                    return render(request, "register.html", {"error": "Bu email allaqachon mavjud!"})

                code = str(random.randint(1000, 9999))
                VerificationCode.objects.filter(email=user_email).delete()
                VerificationCode.objects.create(email=user_email, code=code)

                send_mail(
                    "Ro‘yxatdan o‘tish tasdiqlash kodi",
                    f"Sizning tasdiqlash kodingiz: {code}",
                    "mutalovnuriddin651@gmail.com",
                    [user_email],
                    fail_silently=False,
                )

                print(f"Tasdiqlash kodi: {code}")

                request.session["verification_email"] = user_email 
                request.session["username"] = username 
                request.session["password"] = password

                return redirect("users:verify") 
        else:
            return render(request, "register.html", {"error": "Email yoki telefon kiritilmagan!"})
    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        print("SALOM LOGIN")
        user_email = request.POST.get("user_email")  
        password = request.POST.get("password")

        if not user_email or not password:
            return render(request, "login.html", {"error": "Email yoki telefon kiritilmagan!"})  

        user = None  

        if "@" in user_email: 
            try:
                user_obj = User.objects.get(email=user_email)
                user = authenticate(request, username=user_obj.username, password=password)  
            except User.DoesNotExist:
                pass  
        else:  
            user_obj = User.objects.filter(phone_number=user_email).first()
            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password) 

        if user:  
            print(f"Login muvaffaqiyatli: {user}")
            login(request, user)
            return redirect("products:home")
        else:
            print("Login xato! User topilmadi yoki parol noto‘g‘ri!")
            return render(request, "login.html", {"error": "Login yoki parol xato!"})

    print("Not a POST request")
    return render(request, "login.html")

@login_required
def home(request):
    return render(request, "index.html")


def verify_view(request):

    if request.method == "GET":
        return render(request, "verify.html")
    
    if request.method == "POST":
        email = request.session.get("verification_email")
        username = request.session.get("username")
        password = request.session.get("password")
        entered_code = request.POST.get("code")

        if not email or not username or not password:
            return render(request, "verify.html", {"error": "Ma'lumotlar topilmadi, qayta ro‘yxatdan o‘ting!"})

        try:
            verification = VerificationCode.objects.get(email=email)

            if entered_code == verification.code:
                user_first_name = generate_first_name()
                user = User.objects.create(username=username, email=email, first_name=user_first_name)
                user.set_password(password)
                user.save()

                login(request, user) 
                verification.delete()

                request.session.pop("verification_email", None)
                request.session.pop("username", None)
                request.session.pop("password", None)

                return redirect("products:home")

            return render(request, "verify.html", {"error": "Kod noto‘g‘ri!"})

        except VerificationCode.DoesNotExist:
            return render(request, "verify.html", {"error": "Tasdiqlash kodini oldin olishingiz kerak!"})

    return HttpResponse("Noto‘g‘ri so‘rov", status=400)


@login_required
def logout_view(request):
    logout(request)
    return redirect("users:login")


def profile_view(request):
    orders = Cart.objects.filter(user=request.user).order_by('-created_at')

    context = {
        "orders": orders
    }
    return render(request, "profile.html", context)



@csrf_exempt
@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user

        user.first_name = request.POST.get('first_name', '')
        user.phone_number = request.POST.get('phone', '') 
        user.date_of_birth = request.POST.get('date_of_birth', None)

        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        user.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)