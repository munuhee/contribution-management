from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_penalties, name='list_penalties'),
    path('add/', views.add_penalty, name='add_penalty'),
    path(
        'update/<int:penalty_id>/',
        views.update_penalty,
        name='update_penalty'
    ),
    path(
        'delete/<int:penalty_id>/',
        views.delete_penalty,
        name='delete_penalty'
    ),
]
