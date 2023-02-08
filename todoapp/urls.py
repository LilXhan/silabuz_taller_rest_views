from rest_framework import routers
from django.urls import path 

from .api import TodoViewSet, DeleteAllTodo, GetAllTodo

router = routers.DefaultRouter()

router.register('todo', TodoViewSet, basename='todo')

urlpatterns = [
    path('todo/delAll', DeleteAllTodo.as_view(), name='delAll'),
    path('todo/getAll', GetAllTodo.as_view(), name='getAll')
]

urlpatterns += router.urls