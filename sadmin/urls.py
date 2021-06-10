"""reportlogin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_home, name="admin_home"),
    path('login/', views.userlogin, name="login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('surveyor-list/<str:filter>/', views.surveyor_list, name="surveyor_list"),
    path('surveyor-details/<int:id>/', views.view_surveyor, name="view_surveyor"),
    path('update-surveyor/<int:id>/', views.update_surveyor, name="update_surveyor"),
    path('remove-surveyor/<int:id>/', views.remove_surveyor, name="remove_surveyor"),
    path('register-surveyor/', views.register_surveyor, name="register_surveyor"),
    path('stock-list/', views.stock_list, name="stock_list"),
    path('stock-remove/<int:id>/', views.stock_remove, name="stock_remove"),
    path('add_new_stock/', views.AddNewStock.as_view(), name="add_new_stock"),
    path('update-stock/<int:id>/', views.Update.as_view(), name="update_stock"),
    path('sell-list/', views.sell_list, name="sell_list"),
    path('add_new_sells/', views.AddNewSells.as_view(), name="add_new_sells"),
    path('sell_details/<int:id>/', views.sell_details, name="sell_details"),
    path('sell_remove/<int:id>/', views.sell_remove, name="sell_remove"),
    path('notification_remove/<int:id>/', views.notification_remove, name="notification_remove"),
    path('notification-list/', views.notification_list, name="notification_list"),

]
