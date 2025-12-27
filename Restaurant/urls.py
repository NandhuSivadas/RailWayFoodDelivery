from django.urls import path
from Restaurant import views

app_name = 'wrestauarant'

urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),

    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_restaurant_profile, name='edit_restaurant_profile'),
    path('profile/change-password/', views.changepassword, name='changepassword'),


    path('add_food/', views.add_food, name='add_food'),
    path('my_foods/', views.restaurant_foods, name='restaurant_foods'),
    path('food_status/<int:food_id>/', views.toggle_food_status, name='toggle_food_status'),

    # NEW
    path('update_food/<int:food_id>/', views.update_food, name='update_food'),
    path('delete_food/<int:food_id>/', views.delete_food, name='delete_food'),

    path('booking-requests/', views.booking_requests, name='booking_requests'),
    path('booking-status/<int:booking_id>/<int:status>/',views.update_booking_status,name='update_booking_status'),
    path('accept-order/<int:id>/', views.accept_order, name='accept_order'),
    path('reject-order/<int:id>/', views.reject_order, name='reject_order'),

    path('accpetedBooking/',views.accepted_bookings,name='acceptedBooking'),

    path('report/', views.report, name='report'),


    path('logout/',views.logout,name='logout'),
]
