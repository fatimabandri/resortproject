from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('rooms/', views.rooms, name='rooms'),

    path('room/<int:id>/', views.room, name='room'),

    path('booking/', views.booking, name='booking'),

    path('report/', views.report, name='report'),

    path('restaurant/', views.restaurant, name='restaurant'),

    path('kitchen/', views.kitchen, name='kitchen'),

    path('kitchen-dashboard/', views.kitchen_dashboard, name='kitchen_dashboard'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('contact/', views.contact, name='contact'),

]