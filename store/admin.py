from django.contrib import admin
from .models import Product, Order, OrderItem, Payment, Coupon

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "brand", "model", "price"]

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'being_delivered', 'refund_requested', 'refund_granted', 'billing_address', 'payment', 'coupon']
    list_display_links = [
        'billing_address', 
        'payment',
        'coupon'
    ]
    list_filter = ['user', 'ordered', 'being_delivered', 'refund_requested', 'refund_granted']

admin.site.register(Product, ProductAdmin)

admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)