from django.contrib import admin
from .models import Product, Order, OrederItem

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "brand", "model", "price"]


admin.site.register(Product, ProductAdmin)

admin.site.register(OrederItem)
admin.site.register(Order)