"""PROJECT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from store.views import discount_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("store.urls")),
    path('accounts/', include('allauth.urls')),
    path("register/", user_views.register, name="register"),
    path("register/2/", user_views.register2, name="register2"),
    path('login/', user_views.login, name="login"),
    path("logout/", user_views.logout, name="logout"),
    path("product-discount/", discount_view, name="discount-view"),

    path("api/products/", include("store.api.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
