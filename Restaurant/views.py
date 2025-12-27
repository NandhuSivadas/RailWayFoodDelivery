from django.shortcuts import render, redirect, get_object_or_404
from Restaurant.models import *
from User.models import *
# Create your views here.


def homepage(request):
    return render(request,'Restaurant/homePage.html')


def profile(request):
    if not request.session.get('rid'):
        return redirect('wguest:login')

    restaurant = tbl_restaurant.objects.get(id=request.session['rid'])
    return render(request, 'Restaurant/profile.html', {'restaurant': restaurant})


# ---------------- EDIT PROFILE (SAME PAGE LOGIC AS USER) ----------------
def edit_restaurant_profile(request):
    if not request.session.get('rid'):
        return redirect('wguest:login')

    restaurant = tbl_restaurant.objects.get(id=request.session['rid'])

    if request.method == "POST":
        restaurant.restaurant_name = request.POST.get('restaurant_name')
        restaurant.owner_name = request.POST.get('owner_name')
        restaurant.phone = request.POST.get('phone')
        restaurant.address = request.POST.get('address')
        restaurant.save()

        return redirect('wrestauarant:profile')

    return render(request, 'Restaurant/profile.html', {
        'restaurant': restaurant,
        'edit': True
    })


def changepassword(request):
    if not request.session.get('rid'):
        return redirect('wguest:login')

    restaurant = tbl_restaurant.objects.get(id=request.session['rid'])

    if request.method == "POST":
        old = request.POST.get('old_password')
        new = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')

        if not check_password(old, restaurant.password):
            msg = "Old password incorrect"
        elif new != confirm:
            msg = "Passwords do not match"
        else:
            restaurant.password = make_password(new)
            restaurant.save()

            # 🔴 LOGOUT AFTER PASSWORD CHANGE
            request.session.flush()
            return redirect('wguest:login')

    return render(request, 'Restaurant/changePassword.html')




















def add_food(request):
    if not request.session.get('rid'):
        return redirect('restaurant_login')

    restaurant = get_object_or_404(
        tbl_restaurant,
        id=request.session['rid']
    )

    if request.method == "POST":
        tbl_food.objects.create(
            restaurant=restaurant,
            food_name=request.POST.get('food_name'),
            category=request.POST.get('category'),
            price=request.POST.get('price'),
            description=request.POST.get('description')
        )
        return redirect('wrestauarant:restaurant_foods')

    return render(request, 'Restaurant/addFood.html')


def update_food(request, food_id):
    if not request.session.get('rid'):
        return redirect('restaurant_login')

    food = get_object_or_404(
        tbl_food,
        id=food_id,
        restaurant_id=request.session['rid']
    )

    if request.method == "POST":
        food.food_name = request.POST['food_name']
        food.category = request.POST['category']
        food.price = request.POST['price']
        food.description = request.POST['description']
        food.save()
        return redirect('wrestauarant:restaurant_foods')

    return render(request, 'Restaurant/updateFood.html', {
        'food': food
    })

def delete_food(request, food_id):
    if not request.session.get('rid'):
        return redirect('restaurant_login')

    food = get_object_or_404(
        tbl_food,
        id=food_id,
        restaurant_id=request.session['rid']
    )

    food.delete()
    return redirect('wrestauarant:restaurant_foods')






def restaurant_foods(request):
    if not request.session.get('rid'):
        return redirect('restaurant_login')

    foods = tbl_food.objects.filter(
        restaurant_id=request.session['rid']
    ).order_by('-created_at')

    return render(request, 'Restaurant/myFoods.html', {
        'foods': foods
    })


def toggle_food_status(request,food_id):
    if not request.session.get('rid'):
        return redirect('restaurant_login')

    food = get_object_or_404(
        tbl_food,
        id=food_id,
        restaurant_id=request.session['rid']
    )

    food.is_available = not food.is_available
    food.save()

    return redirect('wrestauarant:restaurant_foods')



def booking_requests(request):
    bookings = tbl_booking.objects.filter(
        restaurant_id=request.session['rid'],
        status=0
    )
    return render(request,'Restaurant/bookingRequest.html', {
        'bookings': bookings
    })


def accept_order(request, id):
    booking = get_object_or_404(tbl_booking, id=id)
    booking.status = 1  # Accepted
    booking.save()
    return redirect('wrestauarant:booking_requests')


def reject_order(request, id):
    booking = get_object_or_404(tbl_booking, id=id)
    booking.status = 2  # Rejected
    booking.save()
    return redirect('wrestauarant:booking_requests')



def update_booking_status(request, booking_id, status):
    booking = tbl_booking.objects.get(
        id=booking_id,
        restaurant_id=request.session['rid']
    )
    booking.status = status
    booking.save()
    return redirect('wrestauarant:booking_requests')


def accepted_bookings(request):
    if not request.session.get('rid'):
        return redirect('wguest:login')

    bookings = tbl_booking.objects.filter(
        restaurant_id=request.session['rid'],
        status=1
    )

    return render(
        request,
        'Restaurant/acceptedBooking.html',
        {'bookings': bookings}
    )

def report(request):
    if not request.session.get('rid'):
        return redirect('wguest:login')

    status_filter = request.GET.get('status')

    bookings = tbl_booking.objects.filter(
        restaurant_id=request.session['rid']
    ).select_related('user', 'food').order_by('-booking_date')

    # Apply status filter
    if status_filter == 'accepted':
        bookings = bookings.filter(status=1)
    elif status_filter == 'rejected':
        bookings = bookings.filter(status=2)
    elif status_filter == 'cancelled':
        bookings = bookings.filter(status=3)
    elif status_filter == 'pending':
        bookings = bookings.filter(status=0)

    return render(request, 'Restaurant/report.html', {
        'bookings': bookings,
        'status_filter': status_filter
    })



def logout(request):
    request.session.flush()
    return redirect('wguest:login')