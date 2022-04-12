from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from attendence.models import Attendence
from attendence.serializers import AttendenceSerializer
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from authentication.permissions import IsAdminOrSupervisorPermission, IsAdminPermission, IsInternPermission
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.
class AttendAPIView(APIView):
    permission_classes = [IsInternPermission]

    def post(self, request):
        now = datetime.now().date()
        attendance, created = Attendence.objects.get_or_create(date=now)
        try:
            attendance.attendees.add(self.request.user)
            return Response({"details":"Attended successfully!"}, status= status.HTTP_202_ACCEPTED)
        except:
            return Response({"details":"Error occoured!"}, status= status.HTTP_409_CONFLICT)

class AttendenceListAPIView(ListAPIView):
    permission_classes = [IsAdminOrSupervisorPermission]
    serializer_class = AttendenceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['date']
    ordering_fields = ['date']
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        qs = Attendence.objects.all()
        return qs

class AttendenceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AttendenceSerializer
    permission_classes = [IsAdminOrSupervisorPermission]
    
    def get_queryset(self):
        return Attendence.objects.all()