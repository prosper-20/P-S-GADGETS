from django.shortcuts import render
from .models import Product
from django.views.generic import ListView, DetailView

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
