from django.urls import path
from . import views


app_name = 'account'
urlpatterns = [
    path('', views.Home.as_view(), name='home-page'),
    path('register/', views.RegisterView.as_view(), name='register-page'),
    path('login/', views.LoginView.as_view(), name='login-page'),
    path('verify/', views.RegisterVerifyView.as_view(), name='verify-page'),
    path('verify-login/', views.VerifyLoginView.as_view(), name='verify-login-page'),
    path('logout/', views.LogOut.as_view(), name='logout-page'),
]

