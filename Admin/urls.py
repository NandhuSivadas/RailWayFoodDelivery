from django.urls import path
from Admin import views
app_name='wadmin'
urlpatterns = [
    path('homepage/',views.homepage,name='homepage'),




    path('restaurant/requests/', views.restaurant_requests, name='restaurant_requests'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurant/status/<int:rid>/<int:status>/',views.change_restaurant_status,name='change_restaurant_status'
    ),

    path('users/', views.user_list, name='user_list'),
    path('user/status/<int:uid>/<int:status>/', views.change_user_status, name='change_user_status'),



    path('orders/', views.order_report, name='order_report'),
    
    path('user-bookings/<int:user_id>/', views.user_booking_history, name='user_booking_history'),

    path('logout/',views.logout,name='logout'),




]
