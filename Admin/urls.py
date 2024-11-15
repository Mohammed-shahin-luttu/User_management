from django.urls import path
from .  import views

urlpatterns = [
    path('adminpanel/',views.my_admin, name='myadmin'),
    path('adminpanel/adduser/', views.add_user, name='adduser'),
    path('adminpanel/edituser/<int:user_id>/',views.edit_user, name='edituser'),
    path('adminpanel/delete/<str:user_id>/',views.delete_user, name='deleteuser'),
]