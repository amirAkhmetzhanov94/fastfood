"""fastfood URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from webapp import views as webapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', webapp_views.Index.as_view()),
    path('orders/', webapp_views.OrdersView.as_view(), name='orders'),
    path('dishes/', webapp_views.DishesView.as_view(), name='dishes'),
    path('orders/<int:pk>/', webapp_views.OrderDetailView.as_view(), name='detail'),
    path('dishes/<int:pk>/delete', webapp_views.DishDeleteView.as_view(), name="delete"),
    path('dishes/new', webapp_views.AddDishView.as_view(), name='add'),
    path('order/<int:pk>/', webapp_views.OrdersMainPage.as_view(), name="orders_main_page")
]