from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name=""),

    path('register', views.register, name="register"),

    path('login', views.mylogin, name="my-login"),

    path('logout', views.user_logout, name="logout"),


    path('dashboard', views.dashboard, name="dashboard"),
    
    path('create-record', views.create_record, name="createData"), 
    
    path('update-record/<int:pk>', views.update_record, name="update-record"), 
    
    path('view-record/<int:pk>', views.read_record, name="view-record"), 




]