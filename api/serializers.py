from rest_framework import serializers
from pmis.models import Client, Project, Task

class ClientSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Client
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    task = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
