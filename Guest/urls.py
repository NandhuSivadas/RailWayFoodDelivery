
from django.contrib import admin
from django.urls import path,include
from Guest import views
app_name='wguest'

urlpatterns = [
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('homepage/',views.homepage,name='homepage'),
    path('restaurant_signup/',views.restaurant_signup,name='restaurant_signup'),

]
