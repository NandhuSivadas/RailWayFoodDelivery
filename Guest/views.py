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


        admin_count = tbl_admin.objects.filter(
            admin_email=email,
            admin_password=password 
        ).count()

        if admin_count > 0:
            admin = tbl_admin.objects.get(admin_email=email)
            request.session['aid'] = admin.id
            return redirect('wadmin:homepage')

        
        try:
            user = tbl_user.objects.get(user_email=email)

            if check_password(password, user.user_password):
                if user.status == 1:
                    request.session['uid'] = user.id
                    request.session['uname'] = user.user_name
                    return redirect('wuser:homepage')
                else:
                    msg = "Your account is blocked. Please contact admin."
            else:
                msg = "Invalid email or password"

        except tbl_user.DoesNotExist:
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

        # Check email already exists
        if tbl_user.objects.filter(user_email=email).exists():
            return render(request, "Guest/Signup.html", {
                "msg": "Email already exists!"
            })

        # Password match check
        if password != confirm_password:
            return render(request, "Guest/Signup.html", {
                "msg": "Passwords do not match!"
            })

        # Hash password
        hashed_password = make_password(password)

        # Create user
        tbl_user.objects.create(
            user_name=name,
            user_email=email,
            user_phone=phone,
            user_password=hashed_password,
            status=1
        )

        return redirect("wguest:login")

    return render(request, "Guest/Signup.html")