from django.db import models
from django.db.models.fields import BooleanField, DecimalField
from django.urls import reverse

CATEGORY_CHOICES = [('drink', 'Напиток'), ('food', 'Еда')]


class Dish(models.Model):
    title = models.CharField(max_length=50)
    category = models.TextField(max_length=15, null=False, blank=False, verbose_name="Category",
                                choices=CATEGORY_CHOICES)
    price = DecimalField(max_digits=10, decimal_places=2)
    activated = BooleanField(default=False)

    def __str__(self):
        return f'{self.title} ({self.category})'

    def get_absolute_url(self):
        return reverse('dishes')

    class Meta:
        verbose_name_plural = "dishes"
        verbose_name = "dish"


class OrderDish(models.Model):
    order = models.ForeignKey('webapp.Order', related_name='order_dishes', on_delete=models.CASCADE,
                              verbose_name='Order')
    dish_in_order = models.ForeignKey('webapp.Dish', related_name='dish_orders', on_delete=models.CASCADE,
                                      verbose_name='Dish')
    qty = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = "Order dishes"


class Order(models.Model):
    dishes = models.ManyToManyField('webapp.Dish', verbose_name='Dish in order',
                                    related_name='orders', through='webapp.OrderDish', through_fields=('order',
                                                                                                       'dish_in_order'),
                                    blank=True)
    completed_order = BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} (Completed Order: {self.completed_order})"
