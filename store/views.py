import imp
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem, BillingAddress
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.


class Home(ListView):
    model = Product
    template_name = 'store/index.html'
    context_object_name = "products"


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }

        return render(self.request, "store/checkout-page.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # ADD FUNCTIONALITY LATER
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country=country,
                    zip = zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect("checkout")
            messages.warning(self.request, "Failed Checkut")
            return redirect('checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            return redirect('order-summary')

    
class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'store/payment.html')

    def post(self, *args, **kwargs):
        token = self.request.POST.get('')
        stripe.Charge.create(
            amount=2000,
            currency='usd',
            source="tok_amex",
            description="Charge for jenny.rose@example.com"
        )

       


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "store/order-summary.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            return redirect('/')


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


@login_required
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
            messages.info(request, "This item quantity has been updated")
            return redirect("order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order-summary")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
                                     ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")


@login_required
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
            messages.info(request, "This item was removed from your cart!")
            return redirect('order-summary')
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("product-detail", slug=slug)

    else:
        messages.info(request, "You do not have an active order.")
        return redirect("product-detail", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
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
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated")
            return redirect('order-summary')
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("product-detail", slug=slug)

    else:
        messages.info(request, "You do not have an active order.")
        return redirect("product-detail", slug=slug)
