from django.shortcuts import render
from .models import Product

# Create your views here.

def home(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, 'store/index.html', context)

def detail(request, slug=None):
    product = Product.objects.get(slug=slug)

    context = {
        "product": product
    }

    return render(request, 'store/product-details.html', context)
