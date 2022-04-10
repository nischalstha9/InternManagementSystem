from django.urls import path
from .views import TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("", TaskListCreateAPIView.as_view(), name="TaskListCreateAPIView"),
    path("<int:pk>/", TaskRetrieveUpdateDestroyAPIView.as_view(), name="TaskListCreateAPIView"),
]
