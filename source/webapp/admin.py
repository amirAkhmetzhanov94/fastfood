from django.contrib import admin
from webapp.models import Dish, Order, OrderDish


class OrderInline(admin.StackedInline):
    model = Order.dishes.through


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "completed_order", "created_at"]
    list_filter = ["id"]
    search_fields = ["id", "dishes"]
    fields = ["id", "completed_order", "created_at"]
    readonly_fields = ["id", "created_at"]

    inlines = [OrderInline]

    def time_seconds(self, obj):
        return obj.created_at.strftime("%d.%m.%Y %H:%M:%S")


admin.site.register(Dish)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDish)
