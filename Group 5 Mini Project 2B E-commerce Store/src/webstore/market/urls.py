from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/<str:query>', views.search, name='search'),
    path('cart/', views.cart, name='cart'),
    path('product/<str:slug>', views.product, name='product'),
    path('logout', views.logoutUser, name='logout'),
    path('empty-cart', views.empty_cart, name='empty-cart'),
]