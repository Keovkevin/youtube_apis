from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.search, name= 'search'),
    path('get_all/', views.get_all, name = 'videos'),

]