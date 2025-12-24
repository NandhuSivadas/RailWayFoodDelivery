from django.urls import path
from Admin import views
app_name='wadmin'
urlpatterns = [
    path('homepage/',views.homepage,name='homepage'),




    path('restaurant/requests/', views.restaurant_requests, name='restaurant_requests'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path(
        'restaurant/status/<int:rid>/<int:status>/',
        views.change_restaurant_status,
        name='change_restaurant_status'
    ),
]
