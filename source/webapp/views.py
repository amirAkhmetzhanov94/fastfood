from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from webapp.models import Dish, Order
from django.urls import reverse, reverse_lazy
from .forms import DishForm
from django.db.models import Q
from django.db.models import Count
from django.db.models import F


class Index(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        dishes = Dish.objects.all()
        return render(request, self.template_name, {"dishes": dishes})

    def post(self, request, *args, **kwargs):
        dishes = Dish.objects.all()
        order_creating = Order.objects.create()
        dish_id = Dish.objects.filter(title=request.POST["dish__title"]).values("id").first()
        order_creating.dish.set(f"{dish_id['id']}")
        orders = Order.objects.filter(id=order_creating.id).values("dish__title", "dish__price").annotate(
            count=Count("dish__title"))
        return render(request, self.template_name, {'dishes': dishes, 'order_id': order_creating.id, "orders": orders})


class OrdersMainPage(View):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        dishes = Dish.objects.all()
        order_id = kwargs["pk"]
        order = Order.objects.get(id=order_id)
        dish = Dish.objects.get(title=request.POST["dish__title"])
        order.dish.add(dish)
        order.save()
        orders = Order.objects.filter(id=order.id).values("dish__title", "dish__price").annotate(count=Count(
            "dish__title"))
        return render(request, self.template_name, {'dishes': dishes, 'order_id': order_id, 'orders': orders})
        # order = Order.objects.filter(id=f"{kwargs['pk']}")
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


class DishesView(TemplateView):
    template_name = 'dishes_list.html'

    def get_context_data(self, **kwargs):
        extra_context = {'dishes': Dish.objects.all()}
        return extra_context


class AddDishView(CreateView):
    template_name = 'dish_add.html'
    form_class = DishForm
    success_url = '/'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class DishDeleteView(DeleteView):
    model = Dish
    template_name = 'dish_delete.html'
    succes_url = reverse_lazy('dishes')


class DishEditView(UpdateView):
    model = Dish
    template_name = 'dish_edit.html'
    fields = '__all__'
