from audioop import add
from django.urls import path

from store.models import Order
from . import views
from .views import add_to_cart, remove_from_cart, OrderSummaryView, remove_single_item_from_cart, CheckoutView, PaymentView, HomeView, AddCouponView, RequestRefundView

urlpatterns = [
    # path("", views.Home.as_view(), name="home"),
    path('', HomeView.as_view(), name='home'),
    path("product/<slug:slug>/", views.Detail.as_view(), name="product-detail"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("add-to-cart/<slug>/", add_to_cart, name="add-to-cart"),
    path("add-coupon/", AddCouponView.as_view(), name="add-coupon"),
    path("remove-from-cart/<slug>/", remove_from_cart, name='remove-from-cart'),
    path("order-summary/", OrderSummaryView.as_view(), name="order-summary"),
    path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart, name="remove-single-item-from-cart"),
    path('payment/<payment_option>/', PaymentView.as_view(), name="payment"),
    path("request-refund/", RequestRefundView.as_view(), name="request-refund")
]