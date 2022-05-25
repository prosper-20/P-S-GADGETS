import imp
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from django.views.generic import ListView, DetailView
from django.utils import timezone


# Create your views here.

class Home(ListView):
    model = Product
    template_name = 'store/index.html'
    context_object_name = "products"


# def home(request):
#     products = Product.objects.all()
#     context = {
#         "products": products
#     }
#     return render(request, 'store/index.html', context)

# def detail(request, slug=None):
#     product = Product.objects.get(slug=slug)

#     context = {
#         "product": product
#     }
#     return render(request, 'store/product-details.html', context)

class Detail(DetailView):
    model = Product
    template_name = "store/product-details.html"
    context_object_name = "product"

def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
        ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("product-detail", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
        else:
            return redirect("product-detail", slug=slug)
            
    else:
        return redirect("product-detail", slug=slug)
    return redirect("product-detail", slug=slug)

