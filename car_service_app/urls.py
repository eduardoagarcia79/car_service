from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new_user', views.new_user),
    path('login', views.login),
    path('logout', views.logout),
    path('details', views.details),
    path('service_new_car', views.service_new_car),
    path('service_existing_car/<int:car_id>', views.service_existing_car),
    path('confirmation/<int:service_id>', views.confirmation),
    path('registration/<int:service_id>', views.registration),
    path('delete/<int:car_id>', views.delete)
]