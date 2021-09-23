from django.db import models
from django.db.models.fields import BooleanField, DecimalField

CATEGORY_CHOICES = [('drink', 'Напиток'), ('food', 'Еда')]


class Dish(models.Model):
    title = models.CharField(max_length=50)
    category = models.TextField(max_length=15, null=False, blank=False, verbose_name="Category",
                                choices=CATEGORY_CHOICES)
    price = DecimalField(max_digits=10, decimal_places=2)
    activated = BooleanField(default=False)


class Order(models.Model):
    dish_in_order = models.ForeignKey('webapp.Dish', on_delete=models.PROTECT, verbose_name='Dish in order',
                                      related_name='orders')  # немного не понял что с ней делать
    completed_order = BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
