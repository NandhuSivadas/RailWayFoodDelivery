from django.shortcuts import render,redirect
from Guest.models import *
# Create your views here.



def restaurant_requests(request):
    restaurants = tbl_restaurant.objects.filter(status=0)
    return render(request, "Admin/restaurant_requests.html",
                  {"restaurants": restaurants})


def approve_restaurant(request, rid):
    tbl_restaurant.objects.filter(id=rid).update(status=1)
    return redirect('restaurant_requests')


def reject_restaurant(request, rid):
    tbl_restaurant.objects.filter(id=rid).update(status=2)
    return redirect('restaurant_requests')
