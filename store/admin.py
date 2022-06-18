from re import U
from django.contrib import admin
from .models import Product, Order, OrderItem, Payment, Coupon, Refund, Address, UserProfile, Comment, Contact

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "brand", "model", "category", "price"]

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)
make_refund_accepted.short_description = "Update orders to refund granted"   


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'being_delivered', 'received', 'refund_requested', 'refund_granted', 'billing_address', 'shipping_address', 'payment', 'coupon']
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address', 
        'payment',
        'coupon'
    ]
    list_filter = ['ordered', 'being_delivered', 'refund_requested', 'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]

    actions = [make_refund_accepted]

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']

admin.site.register(Product, ProductAdmin)

admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)

admin.site.register(UserProfile)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'product', 'date_added')
    list_filter = ('name', 'date_added')
    search_fields = ('name', 'body')


class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "message"]


admin.site.register(Contact, ContactAdmin)
    