from audioop import add
from django.urls import path

from store.models import Order
from . import views
from .views import add_to_cart, remove_from_cart, OrderSummaryView

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("product/<slug:slug>/", views.Detail.as_view(), name="product-detail"),
    path("add-to-cart/<slug>/", add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<slug>/", remove_from_cart, name='remove-from-cart'),
    path("order-summary/", OrderSummaryView.as_view(), name="order-summary")
]