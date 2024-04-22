from django.urls import path, include
from . import views

urlpatterns = [
    path('register/1', views.registerUSeller, name='reguseller'),
    path('register/2', views.registerSeller, name='regseller'),
    path('profile', views.sellerProfile, name='sellerprofile'),

    path('dashboard', views.Dashboard, name='dashboard'),
]
