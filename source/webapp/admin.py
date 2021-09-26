from django.contrib import admin
from webapp.models import Dish, Order, OrderDish

admin.site.register(Dish)
admin.site.register(Order)
admin.site.register(OrderDish)