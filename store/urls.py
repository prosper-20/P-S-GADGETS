from audioop import add
from django.urls import path

from store.models import Order
from . import views
from .views import add_to_cart, remove_from_cart, OrderSummaryView, remove_single_item_from_cart, CheckoutView, PaymentView, HomeView, AddCouponView, RequestRefundView, phone_view, accessories_view, computing_view, camera_view, tablets_view, discount_view, food_view, clothing_view, sound_view, search_products, tester, home_and_kitchen, ProductCommentView

urlpatterns = [
    # path("", views.Home.as_view(), name="home"),
    path('', HomeView.as_view(), name='home'),
    path('search/', views.search_products, name="search_products"),
    path("product/<slug:slug>/", views.Detail.as_view(), name="product-detail"),
    path("product/<slug:slug>/comment/", ProductCommentView.as_view(), name="product-comment"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("add-to-cart/<slug>/", add_to_cart, name="add-to-cart"),
    path("add-coupon/", AddCouponView.as_view(), name="add-coupon"),
    path("remove-from-cart/<slug>/", remove_from_cart, name='remove-from-cart'),
    path("order-summary/", OrderSummaryView.as_view(), name="order-summary"),
    path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart, name="remove-single-item-from-cart"),
    path('payment/<payment_option>/', PaymentView.as_view(), name="payment"),
    path("request-refund/", RequestRefundView.as_view(), name="request-refund"),
    path("category/phones/", phone_view, name="phone_view"),
    path("category/accessory/", accessories_view, name="accessories_view"),
    path("category/tablets/", tablets_view, name="tablets-view"),
    path("category/camera/", camera_view, name="camera-view"),
    path("category/clothing/", clothing_view, name="clothing-view"),
    path("category/computing/", computing_view, name="computing-view"),
    path("category/home-and-kitchen/", home_and_kitchen, name="home_and_kitchen"),
    path("category/sound_and_vision/", sound_view, name="sound-view"),
    path("category/food-beverages/", food_view, name="food-view"),
    path("product/discount/", discount_view, name="discount-view"),

    path("tester/", tester, name="tester")
]