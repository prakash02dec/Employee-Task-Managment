# Import necessary modules and classes
from rest_framework import serializers
from employees.models import Employee
from .models import Task

# Serializer for the Task model
class TaskSerializer(serializers.ModelSerializer):
    # The assignee field is a SlugRelatedField which represents the related Employee object by its 'name' field
    # The queryset for this field includes all Employee objects
    # This field is not required
    assignee = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='name', required=False) 

    # Meta class for the TaskSerializer
    class Meta:
        # The model being serialized is the Task model
        model = Task
        # The fields to be included in the serialized output
        fields = ['id', 'title', 'deadline', 'description', 'assignee'] 
        # The 'assignee' field is not required
        extra_kwargs = {'assignee': {'required': False}}