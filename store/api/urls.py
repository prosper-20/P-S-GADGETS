from django.urls import path
from .views import api_create_view, api_delete_view, api_detail_view, api_list_view, api_update_view


urlpatterns = [
    path("", api_list_view, name="list"),
    path("<slug:slug>/", api_detail_view, name="detail"),
    path("<slug:slug>/update", api_update_view, name="update"),
    path("<slug:slug>/delete", api_delete_view, name="create"),
    path("create", api_create_view, name="create"),
]