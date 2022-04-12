from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,UpdateAPIView
from authentication.permissions import IsAdminOrSupervisorPermission, IsInternPermission, IsTaskOwnerOrReadOnlyPermission, IsTaskOwnerPermission, ReadOnly, is_user_admin, is_user_intern
from task.models import Task
from task.serializers import AssignTaskValidateSerializer, TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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
            qs = self.request.user.task_obj.all()
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
            qs = self.request.user.task_obj.all()
        else:
            qs = Task.objects.filter(supervisor=self.request.user.id)
        return qs

class AssignTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = AssignTaskValidateSerializer(data = data)
        if serializer.is_valid(raise_exception=True):
            tasks = Task.objects.filter(id = data.get('task'))
            if len(tasks)<1:
                return Response({"detail":"TASK NOT FOUND"}, status=status.HTTP_400_BAD_REQUEST)
            task =tasks[0]
            if task.supervisor != self.request.user:
                return Response({"detail":"You do not have permission"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                task.interns.set(data.get('interns'))
            except Exception as e:
                print(e)
                return Response({"detail":"Invalid Interns!"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class TaskCompleteToggleView(UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated,IsInternPermission|IsTaskOwnerPermission]
    
    def get_queryset(self):
        if is_user_admin(self.request):
            qs = Task.objects.all()
        elif is_user_intern(self.request):
            qs = self.request.user.task_obj.all()
            return qs
        else:
            qs = Task.objects.filter(supervisor=self.request.user.id)
        return qs

    def patch(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            obj.complete = not obj.complete
            obj.save()
            serializer = TaskSerializer(obj)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            return Response({"detail":"An error ouccoured!"}, status=status.HTTP_409_CONFLICT)

    def put(self, request, *args, **kwargs):
        return self.patch(self, request, *args, **kwargs)