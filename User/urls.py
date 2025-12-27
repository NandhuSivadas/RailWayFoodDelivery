
from django.contrib import admin
from django.urls import path,include
from User import views
app_name='wuser'

urlpatterns = [
    path('homepage',views.homepage,name="homepage"),

    path('profile/', views.profile,name='profile'),
    path('profile/change-password/', views.change_password,name='change_password'),

    path('select-station/', views.select_station, name='select_station'),
    path('foods-by-station/', views.foods_by_station, name='foods_by_station'),
   
    path('cancel-booking/<int:booking_id>/',views.cancel_booking,name='cancel_booking'),

    path('book-food/<int:food_id>/', views.book_food, name='book_food'),
    path('order-success/', views.order_success, name='order_success'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),

    path('view-menu/<int:rid>/', views.view_food_items, name='view_food_items'),

    path('view-food/<int:rid>/', views.view_food_items, name='view_food_items'),

    path('confirm-order/<int:food_id>/', views.confirm_order, name='confirm_order'),

    path('logout/',views.logout,name='logout'),

    

]
