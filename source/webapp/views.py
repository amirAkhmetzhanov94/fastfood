from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from webapp.models import Dish, Order
from django.db.models import Q
from django.db.models import Count


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        extra_context = {'dishes': Dish.objects.all(), 'number_of_dishes': 0}
        if Order.objects.all():
            extra_context['number_of_dishes'] = Order.objects.count()
            dishes_count = Order.objects.values('dish_in_order__title', 'dish_in_order__price').annotate(
                count=Count('dish_in_order__title'))
            extra_context['total_price'] = 0
            for total_price in dishes_count:
                extra_context['total_price'] += (total_price["dish_in_order__price"] * total_price["count"])
            extra_context['dishes_count'] = dishes_count
        return extra_context


class OrdersView(TemplateView):
    template_name = 'orders_list.html'

    def get_context_data(self, **kwargs):
        extra_context = {"orders": Order.objects.all()}
        return extra_context
