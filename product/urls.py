from django.urls import path
from .views import (
    ProductsListAPIView,
    ProductDetailAPIView,
    CategoryListAPIView,
    CategoryDetailAPIView,
    ReviewListAPIView,
    ReviewDetailAPIView,
    ProductReviewsAPIView,
    AverageRatingAPIView
)

from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductsListAPIView.as_view()),
    path('<int:id>/', views.ProductDetailAPIView.as_view()),

]