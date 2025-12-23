from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from Guest.models import *
from Admin.models import *


def homepage(request):
    return render(request,'Guest/homepage.html')



def login(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_pass")

        # 🔐 ADMIN LOGIN (Plain Password)
        admin = tbl_admin.objects.filter(
            admin_email=email,
            admin_password=password
        ).first()

        if admin:
            request.session.flush()
            request.session['aid'] = admin.id
            return redirect('wadmin:homepage')

        # 👤 USER LOGIN (Hashed Password)
        user = tbl_user.objects.filter(
            user_email=email
        ).first()

        if user:
            if check_password(password, user.user_password):
                if user.status == 1:
                    request.session.flush()
                    request.session['uid'] = user.id
                    request.session['uname'] = user.user_name
                    return redirect('wuser:homepage')
                else:
                    msg = "Your user account is blocked"
                    return render(request, 'Guest/Login.html', {'msg': msg})
            else:
                msg = "Invalid email or password"
                return render(request, 'Guest/Login.html', {'msg': msg})

        # 🏨 RESTAURANT LOGIN (Hashed Password + Admin Approval)
        restaurant = tbl_restaurant.objects.filter(
            email=email
        ).first()

        if restaurant:
            if check_password(password, restaurant.password):
                if restaurant.status == 1:
                    request.session.flush()
                    request.session['rid'] = restaurant.id
                    request.session['rname'] = restaurant.restaurant_name
                    return redirect('wrestauarant:homepage')
                else:
                    msg = "Restaurant not approved by admin"
                    return render(request, 'Guest/Login.html', {'msg': msg})
            else:
                msg = "Invalid email or password"
                return render(request, 'Guest/Login.html', {'msg': msg})

        # ❌ NO MATCH FOUND
        msg = "Invalid email or password"
        return render(request, 'Guest/Login.html', {'msg': msg})

    return render(request, 'Guest/Login.html')




def signup(request):
    if request.method == "POST":
        name = request.POST.get("txt_name")
        email = request.POST.get("txt_email")
        phone = request.POST.get("txt_phone")
        password = request.POST.get("txt_password")
        confirm_password = request.POST.get("txt_confirm_password")

      
        if tbl_user.objects.filter(user_email=email).exists():
            return render(request, "Guest/Signup.html", {
                "msg": "Email already exists!"
            })

     
        if password != confirm_password:
            return render(request, "Guest/Signup.html", {
                "msg": "Passwords do not match!"
            })

        # Hash password
        hashed_password = make_password(password)

        tbl_user.objects.create(
            user_name=name,
            user_email=email,
            user_phone=phone,
            user_password=hashed_password,
            status=1
        )

        return redirect("wguest:login")

    return render(request, "Guest/Signup.html")

def restaurant_signup(request):
    if request.method == "POST":
        restaurant_name = request.POST['restaurant_name']
        owner_name = request.POST['owner_name']
        email = request.POST['email']
        phone = request.POST['phone']
        station_name = request.POST['station_name']
        station_code = request.POST['station_code']
        address = request.POST['address']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, "Admin/restaurant_signup.html",
                          {"msg": "Passwords do not match"})

        if tbl_restaurant.objects.filter(email=email).exists():
            return render(request, "Admin/restaurant_signup.html",
                          {"msg": "Email already registered"})

        tbl_restaurant.objects.create(
            restaurant_name=restaurant_name,
            owner_name=owner_name,
            email=email,
            phone=phone,
            station_name=station_name,
            station_code=station_code,
            address=address,
            password=make_password(password),
            status=0   # Pending approval
        )

        return render(request, "Guest/restaurantSignUp.html",
                      {"msg": "Registration successful! Waiting for admin approval."})

    return render(request, "Guest/restaurantSignUp.html")
