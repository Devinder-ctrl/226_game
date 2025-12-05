from django.urls import path
from . import views

urlpatterns = [
 
    path('', views.index, name='index'),
     path('Two/<str:name>', views.check_player, name='Two'),
     path('One/<str:name>', views.check_player, name='One'),
    path('players/', views.home, name='home'),
    path('create/', views.final, name='create'),
    
    path('pick/<str:name>/<int:row>/<int:col>/' , views.pick, name='pick'),
    
]
