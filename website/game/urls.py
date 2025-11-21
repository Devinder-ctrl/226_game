from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.index, name='index'),
    path('create/', views.final, name='index'),
    path('pick/<str:name>/<int:row>/<int:col>/' , views.pick, name='pick'),

]
