from django.urls import path
from Admin import views

urlpatterns = [
    path('restaurant/requests/', views.restaurant_requests, name='restaurant_requests'),
    path('restaurant/approve/<int:rid>/', views.approve_restaurant, name='approve_restaurant'),
    path('restaurant/reject/<int:rid>/', views.reject_restaurant, name='reject_restaurant'),
]
