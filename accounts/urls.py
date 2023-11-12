from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view()),
    path('signup/', views.SignupAPIView.as_view()),
    path('users/confirm/<int:userid>/', views.ConfirmUserAPIView.as_view()),
]