from django.contrib import admin
from .models import Product, Order, OrderItem, Payment

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "brand", "model", "price"]

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']

admin.site.register(Product, ProductAdmin)

admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)