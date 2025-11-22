from django.urls import path
from . import views

urlpatterns = [
   
    #Show current board and players
    path('', views.index, name='index'),
    #create board and initialize players
    path('create/', views.final, name='index'),
    #for picking tiles at given row and column
    path('pick/<str:name>/<int:row>/<int:col>/' , views.pick, name='pick'),

]
