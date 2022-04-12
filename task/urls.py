from django.urls import path
from .views import AssignTaskAPIView, TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView, TaskCompleteToggleView

urlpatterns = [
    path("", TaskListCreateAPIView.as_view(), name="TaskListCreateAPIView"),
    path("<int:pk>/", TaskRetrieveUpdateDestroyAPIView.as_view(), name="TaskListCreateAPIView"),
    path("assign/", AssignTaskAPIView.as_view(), name="AssignTaskAPIView"),
    path("<int:pk>/toggleComplete/", TaskCompleteToggleView.as_view(), name="TaskCompleteToggleView"),
]
