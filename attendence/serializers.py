from rest_framework import serializers
from .models import Attendence

class AttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendence
        fields = "__all__"