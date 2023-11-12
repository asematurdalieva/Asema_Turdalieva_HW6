"""
URL configuration for appi_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from product import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/categories/', views.CategoryListAPIView.as_view()),
    path('api/v1/categories/<int:category_id>/', views.CategoryDetailAPIView.as_view()),
    path('api/v1/products/', include('product.urls')),
    path('api/v1/products/<int:product_id>/', views.ProductsListAPIView.as_view()),
    path('api/v1/reviews/', views.ReviewListAPIView.as_view()),
    path('api/v1/reviews/<int:review_id>/', views.ReviewDetailAPIView.as_view()),
    path('api/v1/products/reviews/', views.ProductsListAPIView.as_view()),
    path('api/v1/products/average_rating/', views.AverageRatingAPIView.as_view()),
    path('api/v1/accounts/', include('accounts.urls')),
]