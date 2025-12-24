from django.shortcuts import render,redirect
from Guest.models import *
# Create your views here.



def homepage(request):
    return render(request,'Admin/homepage.html')



def restaurant_requests(request):
    restaurants = tbl_restaurant.objects.filter(status=0)
    return render(request, "Admin/restaurant_requests.html",
                  {"restaurants": restaurants})

from django.shortcuts import render, redirect, get_object_or_404
from Guest.models import tbl_restaurant

def restaurant_list(request):
    if not request.session.get('aid'):
        return redirect('wguest:login')

    status_filter = request.GET.get('status')

    restaurants = tbl_restaurant.objects.all().order_by('-id')

    if status_filter == 'accepted':
        restaurants = restaurants.filter(status=1)
    elif status_filter == 'rejected':
        restaurants = restaurants.filter(status=2)
    elif status_filter == 'pending':
        restaurants = restaurants.filter(status=0)

    return render(request, 'Admin/RestaurantList.html', {
        'restaurants': restaurants,
        'status_filter': status_filter
    })


def change_restaurant_status(request, rid, status):
    if not request.session.get('aid'):
        return redirect('wguest:login')

    restaurant = get_object_or_404(tbl_restaurant, id=rid)
    restaurant.status = status
    restaurant.save()

    return redirect('wadmin:restaurant_list')
