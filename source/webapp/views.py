from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from webapp.models import Dish, Order, OrderDish
from django.urls import reverse_lazy
from .forms import DishForm


class Index(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        dishes = Dish.objects.all()
        return render(request, self.template_name, {"dishes": dishes})

    def post(self, request, *args, **kwargs):
        dishes = Dish.objects.all()
        order = Order.objects.create()
        dish_id = get_object_or_404(Dish, id=request.POST["dish_id"])
        order.dishes.add(dish_id)
        dish_orders = order.order_dishes.all().values("dish_in_order__title", "dish_in_order__price", "qty", "id")
        return render(request, self.template_name, {'dishes': dishes, 'order_id': order.id, "dish_orders":
            dish_orders, "total_price": dish_id.price})


class OrdersMainPage(View):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        dishes = Dish.objects.all()
        order_id = kwargs["pk"]
        order = Order.objects.get(id=order_id)
        dish = None
        try:
            dish_for_delete = request.POST.get("dish_delete")
            if dish_for_delete:
                dish = OrderDish.objects.get(order_id=order_id, pk=request.POST['dish_delete'])
                dish.delete()
                orderdish = OrderDish.objects.filter(order_id=order_id)
                if not len(orderdish):
                    order = Order.objects.get(id=order_id)
                    order.delete()
                    return redirect('index')
                dish_orders = order.order_dishes.all().values("dish_in_order__title", "dish_in_order__price", "qty",
                                                              "id")
                return render(request, self.template_name, {'dishes': dishes, 'order_id': order_id, 'dish_orders':
                    dish_orders, "total_price": self.get_total_sum(dish_orders)})

            dish = OrderDish.objects.get(order_id=order_id, dish_in_order_id=request.POST["dish_id"])
            dish.qty += 1
            dish.save()
        except Exception as e:
            print(e)
            dish = Dish.objects.get(id=request.POST["dish_id"])
            order.dishes.add(dish)
        dish_orders = order.order_dishes.all().values("dish_in_order__title", "dish_in_order__price", "qty", "id")
        return render(request, self.template_name, {'dishes': dishes, 'order_id': order_id, 'dish_orders':
            dish_orders, "total_price": self.get_total_sum(dish_orders)})

    def get_total_sum(self, orders):
        total = 0
        for o in orders:
            total += o['qty'] * o['dish_in_order__price']
        return total


class OrdersView(TemplateView):
    template_name = 'orders_list.html'

    def get_context_data(self, **kwargs):
        dish_orders = OrderDish.objects.all().values("dish_in_order__title", "dish_in_order__price", "qty", "id")
        extra_context = {"total_sum": self.get_total_sum(dish_orders), "orders": Order.objects.all()}
        return extra_context

    def get_total_sum(self, orders):
        total = 0
        for o in orders:
            # print(o['qty'])
            # print(o['dish_in_order__price'])
            total += o['qty'] * o['dish_in_order__price']
        return total


class OrderDetailView(View):
    template_name = 'order_detail.html'

    def get(self, request, *args, **kwargs):
        dish_order = OrderDish.objects.filter(order_id=kwargs["pk"])
        total_sum = 0
        for dish in dish_order:
            total_sum += dish.dish_in_order.price * dish.qty

        return render(request, self.template_name, {"dish_order": dish_order, "order_id": kwargs["pk"], "total_sum":
            total_sum})

    def post(self, request, *args, **kwargs):
        dish_order = OrderDish.objects.filter(order_id=kwargs["pk"])
        total_sum = 0
        for dish in dish_order:
            total_sum += dish.dish_in_order.price * dish.qty
        order = get_object_or_404(Order, pk=kwargs["pk"])
        is_completed = request.POST.get("is_completed")
        if is_completed:
            order.completed_order = True
            order.save()
            return render(request, self.template_name, {"dish_order": dish_order, "order_id": kwargs["pk"], "total_sum":
                total_sum, "completed_order": order.completed_order})


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
