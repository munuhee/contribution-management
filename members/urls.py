from django.urls import path
from .views import (
    list_members, add_member,
    update_member, delete_member, member_detail
)

urlpatterns = [
    path('', list_members, name='list_members'),
    path('<int:member_id>/', member_detail, name='member_detail'),
    path('add/', add_member, name='add_member'),
    path('update/<int:member_id>/', update_member, name='update_member'),
    path('delete/<int:member_id>/', delete_member, name='delete_member'),
]
