
from django.contrib import admin
from django.urls import path,include
from User import views
app_name='wuser'

urlpatterns = [
    path('homepage',views.homepage,name="homepage"),
    

]
