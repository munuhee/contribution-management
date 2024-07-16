from django.urls import path
from .views import list_cases, add_case, update_case, delete_case

urlpatterns = [
    path('', list_cases, name='list_cases'),
    path('add/', add_case, name='add_case'),
    path('update/<int:case_id>/', update_case, name='update_case'),
    path('delete/<int:case_id>/', delete_case, name='delete_case'),
]
