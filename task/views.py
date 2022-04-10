from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from authentication.permissions import IsAdminOrSupervisorPermission, IsTaskOwnerOrReadOnlyPermission, ReadOnly, is_user_admin, is_user_intern
from task.models import Task
from task.serializers import TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.
class TaskListCreateAPIView(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrSupervisorPermission|ReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['supervisor']
    search_fields = ['name',]
    ordering_fields = ['name','created_at']
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if is_user_admin(self.request):
            qs = Task.objects.all()
        elif is_user_intern(self.request):
            qs = Task.objects.filter(intern = self.request.user.id)
        else:
            qs = Task.objects.filter(supervisor=self.request.user.id)
        return qs

class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsTaskOwnerOrReadOnlyPermission]
    
    def get_queryset(self):
        if is_user_admin(self.request):
            qs = Task.objects.all()
        elif is_user_intern(self.request):
            qs = Task.objects.filter(intern = self.request.user.id)
        else:
            qs = Task.objects.filter(supervisor=self.request.user.id)
        return qs