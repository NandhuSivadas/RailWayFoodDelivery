from django.shortcuts import render, redirect, get_object_or_404
from Guest.models import *
from User.models import *
from django.db.models import Q,Max

# Create your views here.



def homepage(request):
    userCount=tbl_user.objects.count()
    accepted_users = tbl_user.objects.filter(status=1).count()
    rejected_users = tbl_user.objects.filter(status=2).count()
    pending_users = tbl_user.objects.filter(status=0).count()
    restaurantCount=tbl_restaurant.objects.count()
    orderCount=tbl_booking.objects.count()
    

    return render(request,'Admin/homepage.html',{"userCount":userCount,"restaurantCount":restaurantCount,"orderCount":orderCount,
        'accepted_users': accepted_users,
        'rejected_users': rejected_users,
        'pending_users': pending_users, })



def restaurant_requests(request):
    restaurants = tbl_restaurant.objects.filter(status=0)
    return render(request, "Admin/restaurant_requests.html",
                  {"restaurants": restaurants})




def restaurant_list(request):
   
    if not request.session.get('aid'):
        return redirect('wguest:login')

    status_filter = request.GET.get('status')   # pending / accepted / rejected
    search = request.GET.get('search')          # search text

    restaurants = tbl_restaurant.objects.all()

    # STATUS FILTER
    if status_filter == 'pending':
        restaurants = restaurants.filter(status=0)
    elif status_filter == 'accepted':
        restaurants = restaurants.filter(status=1)
    elif status_filter == 'rejected':
        restaurants = restaurants.filter(status=2)

    # SEARCH FILTER (ANY FIELD)
    if search:
        restaurants = restaurants.filter(
            Q(restaurant_name__icontains=search) |
            Q(owner_name__icontains=search) |
            Q(email__icontains=search) |
            Q(station_name__icontains=search) |
            Q(station_code__icontains=search)
        )

    restaurants = restaurants.order_by('-id')

    return render(request, 'Admin/restaurantList.html', {
        'restaurants': restaurants,
        'status_filter': status_filter,
        'search': search
    })



def change_restaurant_status(request, rid, status):
    if not request.session.get('aid'):
        return redirect('wguest:login')

    restaurant = get_object_or_404(tbl_restaurant, id=rid)
    restaurant.status = status
    restaurant.save()

    return redirect('wadmin:restaurant_list')




def user_list(request):
    if not request.session.get('aid'):
        return redirect('wguest:login')

    status_filter = request.GET.get('status')

    users = tbl_user.objects.all().order_by('-id')

    if status_filter == 'accepted':
        users = users.filter(status=1)
    elif status_filter == 'rejected':
        users = users.filter(status=2)
    elif status_filter == 'pending':
        users = users.filter(status=0)

    return render(request, 'Admin/userList.html', {
        'users': users,
        'status_filter': status_filter
    })


def change_user_status(request, uid, status):
    if not request.session.get('admin_id'):
        return redirect('wguest:login')

    tbl_user.objects.filter(id=uid).update(status=status)
    return redirect('wadmin:userList')


# def order_report(request):
#     status = request.GET.get('status')
#     search = request.GET.get('search')
#     from_date = request.GET.get('from_date')
#     to_date = request.GET.get('to_date')

#     # STEP 1: Get latest booking date per user
#     latest_bookings = (
#         tbl_booking.objects
#         .values('user_id')
#         .annotate(latest_date=Max('booking_date'))
#     )

#     # STEP 2: Get actual booking records
#     bookings = tbl_booking.objects.filter(
#         booking_date__in=[b['latest_date'] for b in latest_bookings]
#     )

#     # STATUS FILTER (optional)
#     if status:
#         status_map = {
#             'pending': 0,
#             'accepted': 1,
#             'rejected': 2,
#             'cancelled': 3
#         }
#         bookings = tbl_booking.filter(status=status_map.get(status))

#     # SEARCH FILTER
#     if search:
#         bookings = tbl_booking.filter(
#             Q(user__user_name__icontains=search) |
#             Q(restaurant__restaurant_name__icontains=search) |
#             Q(food__food_name__icontains=search)
#         )

#     # DATE FILTER (optional)
#     if from_date and to_date:
#         bookings = tbl_booking.filter(booking_date__date__range=[from_date, to_date])

#     context = {
#         'bookings': bookings.order_by('-booking_date'),
#         'status_filter': status,
#         'search': search,
#         'from_date': from_date,
#         'to_date': to_date,
#     }

#     return render(request, 'Admin/orderReport.html', context)

def order_report(request):
    status = request.GET.get('status')
    search = request.GET.get('search')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    # STEP 1: Use .objects for the query manager
    latest_bookings = (
        tbl_booking.objects.values('user_id')
        .annotate(latest_date=Max('booking_date'))
    )

    # STEP 2: Use actual booking records
    bookings = tbl_booking.objects.filter(
        booking_date__in=[b['latest_date'] for b in latest_bookings]
    )

    # STATUS FILTER - Change tbl_booking.filter to bookings.filter
    if status:
        status_map = {'pending': 0, 'accepted': 1, 'rejected': 2, 'cancelled': 3}
        bookings = bookings.filter(status=status_map.get(status))

    # SEARCH FILTER - Use .objects if starting a new query, or chain from bookings
    if search:
        bookings = bookings.filter(
            Q(user__user_name__icontains=search) |
            Q(restaurant__restaurant_name__icontains=search) |
            Q(food__food_name__icontains=search)
        )

    # DATE FILTER
    if from_date and to_date:
        bookings = bookings.filter(booking_date__date__range=[from_date, to_date])

    context = {
        'bookings': bookings.order_by('-booking_date'),
        'status_filter': status,
        'search': search,
        'from_date': from_date,
        'to_date': to_date,
    }
    return render(request, 'Admin/orderReport.html', context)




def user_booking_history(request, user_id):
    bookings = tbl_booking.objects.filter(user_id=user_id).order_by('-booking_date')

    return render(request, 'Admin/userBookingHistory.html', {
        'bookings': bookings
    })



def logout(request):
    request.session.flush()
    return redirect('wguest:login')