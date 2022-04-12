from django.urls import path
from .views import AttendAPIView, AttendenceListAPIView,AttendenceRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("attend/", AttendAPIView.as_view(), name="AttendanceAttendAPIView"),
    path("<int:pk>/", AttendenceRetrieveUpdateDestroyAPIView.as_view(), name="AttendenceRetrieveUpdateDestroyAPIView"),
    path("", AttendenceListAPIView.as_view(), name="AttendanceListAPIView"),
    
]
