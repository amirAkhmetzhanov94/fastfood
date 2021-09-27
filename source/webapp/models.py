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


class Order(models.Model):
    dish = models.ManyToManyField('webapp.Dish', verbose_name='Dish in order',
                                  related_name='orders')
    completed_order = BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} (Completed Order: {self.completed_order})"
