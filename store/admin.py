from django.contrib import admin
from .models import Product, Order, OrderItem

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "brand", "model", "price"]


admin.site.register(Product, ProductAdmin)

admin.site.register(OrderItem)
admin.site.register(Order)