from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('outlet/<int:outlet_id>/', views.outlet_inventory, name='outlet_inventory'),
]