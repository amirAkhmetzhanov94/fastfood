from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from webapp.models import Dish, Order


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        extra_context = {'Orders': Order.objects.all()}
        return extra_context
