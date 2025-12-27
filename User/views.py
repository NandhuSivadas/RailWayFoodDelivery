from django.shortcuts import render,redirect,get_object_or_404
from Guest.models import *
from Restaurant.models import *
from User.models import *

# Create your views here.


def homepage(request):
    stations = tbl_restaurant.objects.filter(
        status=1
    ).values_list('station_name', flat=True).distinct()
    return render(request, 'User/homePage.html', {
        'stations': stations})



def profile(request):
    if not request.session.get('uid'):
        return redirect('wguest:login')
    user = tbl_user.objects.get(id=request.session['uid'])
    edit_mode = request.GET.get('edit') == '1'

    if request.method == 'POST':
        user.user_name = request.POST['user_name']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.save()
        return redirect('wuser:profile')
    return render(request, 'User/profile.html', {
        'user': user,
        'edit_mode': edit_mode
    })


def change_password(request):
    if not request.session.get('uid'):
        return redirect('wguest:login')
    user = tbl_user.objects.get(id=request.session['uid'])
    msg = ""
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        # Check current password
        if not check_password(current_password, user.user_password):
            msg = "Current password is incorrect"
        elif new_password != confirm_password:
            msg = "New password and confirm password do not match"
        else:
            user.user_password = make_password(new_password)
            user.save()
            # OPTIONAL: logout user after password change
            del request.session['uid']
            del request.session['uname']
            return redirect('wguest:login')
    return render(request, 'User/changePassword.html', {'msg': msg})



def select_station(request):
    stations = tbl_restaurant.objects.filter(
        status=1
    ).values_list('station_name', flat=True).distinct()
    return render(request, 'User/selectStation.html', {
        'stations': stations
    })



# def foods_by_station(request):
#     station = request.GET.get('station')
#     foods = tbl_food.objects.filter(
#         restaurant__station_name=station,
#         restaurant__status=1,
#         is_available=True
#     ).select_related('restaurant')

#     return render(request, 'User/FoodsByStation.html', {
#         'foods': foods,
#         'station': station
#     })




def foods_by_station(request):

    station = request.GET.get('station')
    restaurants = tbl_restaurant.objects.filter(
        station_name__icontains=station, 
        status=1
    )

    context = {
        'station': station,
        'restaurants': restaurants,
    }
    
    return render(request, 'User/selectRestaurant.html', context)


def view_food_items(request, rid):
    # Fetch the restaurant or return 404 if not found
    restaurant = get_object_or_404(tbl_restaurant, id=rid)
    
    # Fetch all food items for this restaurant
    # Assuming your food model has a foreign key to tbl_restaurant
    foods = tbl_food.objects.filter(restaurant=restaurant)
    
    context = {
        'restaurant': restaurant,
        'foods': foods,
    }
    return render(request, 'User/menu.html', context)







def book_food(request, food_id):
    if not request.session.get('uid'):
        return redirect('wguest:login')
    food = get_object_or_404(tbl_food, id=food_id)
    user = tbl_user.objects.get(id=request.session['uid'])
    # 🔹 STEP 1: Show quantity & time page
    if request.method == 'GET':
        return render(request, 'User/ConfirmBooking.html', {
            'food': food
        })

    # 🔹 STEP 2: Save booking and go to success page
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        delivery_time = request.POST['delivery_time']

        total_price = food.price * quantity
        tbl_booking.objects.create(
            user=user,
            restaurant=food.restaurant,
            food=food,
            quantity=quantity,
            delivery_time=delivery_time,
            price=total_price,
            status=0
        )
        return redirect('wuser:order_success')



def my_bookings(request):
    if not request.session.get('uid'):
        return redirect('wguest:login')
    bookings = tbl_booking.objects.filter(
        user_id=request.session['uid']
    ).order_by('-booking_date')

    # Attach timer flags
    for b in bookings:
        b.can_cancel_flag = b.can_cancel()
        b.cancel_deadline_ts = int(b.cancel_deadline().timestamp())

    return render(request, 'User/MyBookings.html', {
        'bookings': bookings
    })



def cancel_booking(request, booking_id):
    if not request.session.get('uid'):
        return redirect('wguest:login')

    booking = get_object_or_404(
        tbl_booking,
        id=booking_id,
        user_id=request.session['uid']
    )
    # ✅ Final backend safety check
    if booking.can_cancel() and booking.status in [0, 1]:
        booking.status = 3  # Cancelled
        booking.save()
    return redirect('wuser:my_bookings')



def order_success(request):
    if not request.session.get('uid'):
        return redirect('wguest:login')
    return render(request, 'User/orderSuccess.html')


def confirm_order(request, food_id):
    if not request.session.get('uid'):
        return redirect('wguest:login')
        
    food = get_object_or_404(tbl_food, id=food_id)
    user = tbl_user.objects.get(id=request.session['uid'])
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        delivery_time_str = request.POST.get('delivery_time')

        # Server-side Time Validation (20-minute buffer)
        if delivery_time_str:
            selected_time = datetime.strptime(delivery_time_str, '%H:%M').time()
            now = timezone.localtime()
            # Combine today's date with selected time
            selected_dt = now.replace(hour=selected_time.hour, minute=selected_time.minute, second=0, microsecond=0)
            
            # If the time selected is earlier than (now + 20 mins), reject it
            if selected_dt < (now + timedelta(minutes=20)):
                return render(request, 'User/ConfirmBooking.html', {
                    'food': food,
                    'msg': 'Delivery time must be at least 20 minutes from now.'
                })

            total_price = food.price * quantity
            tbl_booking.objects.create(
                user=user,
                restaurant=food.restaurant,
                food=food,
                quantity=quantity,
                delivery_time=delivery_time_str,
                price=total_price,
                status=0
            )
            return redirect('wuser:order_success')

    # GET request: show the confirmation card
    return render(request, 'User/ConfirmBooking.html', {'food': food})




def logout(request):
    request.session.flush()
    return redirect('wguest:login')