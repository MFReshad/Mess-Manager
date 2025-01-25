from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),

    path('register', views.register_user_mess, name="register"),

    path('login', views.mylogin, name="my-login"),

    path('logout', views.user_logout, name="logout"),


    path('dashboard', views.dashboard, name="dashboard"),
    
    path('create-record', views.create_record, name="createData"), 
    
    path('update-record/<int:pk>', views.update_record, name="update-record"), 
    
    path('view-record/<int:pk>', views.read_record, name="view-record"), 
    
    path('delete-record/<int:pk>', views.delete_record, name="delete-record"), 
    
    # mess

    path('create-mess', views.create_mess, name="create_mess"), 

    #### bazar ####
    # view bazar list (User ,Admin)
    path('bazar-list', views.bazar_list, name="bazar-list"),
    
    path('bazar-list/<str:date>', views.bazar_list_date, name="bazar-list-date"),

    # add bazar
    path('<str:mess_name_slug>/add_bazar_list/', views.add_bazar, name="add_bazar_list"),


]