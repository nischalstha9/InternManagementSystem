from django.urls import path
from .views import AttendAPIView, AttendenceListAPIView

urlpatterns = [
    path("attend/", AttendAPIView.as_view(), name="AttendanceAttendAPIView"),
    path("", AttendenceListAPIView.as_view(), name="AttendanceListAPIView"),
]
