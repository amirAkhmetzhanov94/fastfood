from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from webapp.models import Dish, Order
from django.db.models import Q
from django.db.models import Count


class Index(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        dishes = Dish.objects.all()
        return render(request, self.template_name, {"dishes": dishes})

    def post(self, request, *args, **kwargs):
        dishes = Dish.objects.all()
        order = Order.objects.create()
        dish_id = Dish.objects.filter(title=request.POST["dish__title"]).values("id").first()
        order.dish.set(f"{dish_id['id']}")
        return render(request, self.template_name, {'dishes': dishes})
    # def get_context_data(self, **kwargs):
    #     extra_context = {'dishes': Dish.objects.all(), 'number_of_dishes': 0}
    #     Order.objects.values("id")
    #     if Order.objects.all():
    #         extra_context['number_of_dishes'] = Order.objects.count()
    #         extra_context['orders'] = Order.objects.values("id")
    #         # dishes_count = Order.objects.values('dish_in_order__title', 'dish_in_order__price').annotate(
    #         #     count=Count('dish_in_order__title'))
    #         extra_context['total_price'] = 0
    #         # for total_price in dishes_count:
    #         #     extra_context['total_price'] += (total_price["dish_in_order__price"] * total_price["count"])
    #         # extra_context['dishes_count'] = dishes_count
    #     return extra_context


class OrdersView(TemplateView):
    template_name = 'orders_list.html'

    def get_context_data(self, **kwargs):
        extra_context = {"orders": Order.objects.all()}
        return extra_context


class OrderDetailView(TemplateView):
    template_name = 'order_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['order'] = get_object_or_404(Order, pk=kwargs['pk'])
        return super().get_context_data(**kwargs)