from typing import Text
from django.db import models
from django.db.models.fields import BooleanField, DecimalField
from django.db.models.fields.related import ForeignKey

class Category:
    category = models.CharField(max_length=20)
    
    def __str__(self):
        return self.category


class Dish: 
    title = models.CharField(max_length=50)
    category = ForeignKey("webapp.Category", verbose_name='category', on_delete=models.PROTECT)
    price = DecimalField(max_digits=10, decimal_places=2)
    activated = BooleanField(default=False)


class Order:
    dish_in_order = models.CharField(max_length=100)  #немного не понял что с ней делать
    completed_order = BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

