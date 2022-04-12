from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        extra_kwargs = {
            "supervisor":{
                "required":False
            },
        }

    def validate(self, attrs):
        user =self.context.get("view").request.user
        print(user)
        attrs['supervisor'] = self.context.get("view").request.user
        return attrs

class AssignTaskValidateSerializer(serializers.Serializer):
    interns = serializers.ListField()
    task = serializers.IntegerField()
