from django.urls import path
from . import views


urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("product/<slug:slug>/", views.Detail.as_view(), name="product-detail")
]