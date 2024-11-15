from django.urls import path
from . import views
urlpatterns = [
    path('',views.Loginpage, name='login'),
    path('home/',views.HomePage, name='home'),
    path('logout/',views.Logout, name='logout'),
    path('signup/',views.SignUp, name='signup'),
    path('shahin/',views.Shahin, name='sha')
]