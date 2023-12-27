import time
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import Employee
from tasks.serializers import TaskSerializer


# Serializer for listing employees
class EmployeeListSerializer(serializers.ModelSerializer):
    # Nested serializer for tasks associated with the employee
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        # Fields to be included in the serialized output
        fields = ['id' ,'name', 'email', 'is_lead' , 'tasks']
        # 'is_lead' and 'tasks' fields are not required
        extra_kwargs = {'is_lead': {'required': False} , 'tasks': {'required': False} }


# Serializer for creating and updating employees
class EmployeeSerializer(serializers.ModelSerializer):
    # Password field that is write-only and validated
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # Nested serializer for tasks associated with the employee
    tasks = TaskSerializer(many=True, read_only=True)


    class Meta:
        model = Employee
        # Fields to be included in the serialized output
        fields = ['id', 'name', 'email', 'password', 'is_lead', 'tasks']
        # 'is_lead' and 'tasks' fields are not required
        extra_kwargs = {
            'is_lead': {'required': False},
            'tasks': {'required': False}
        }

    # Method for creating a new employee
    def create(self, validated_data):
        # Generate a unique username by appending the current timestamp to the email
        username = validated_data['email'] + str(int(time.time()))
        # Create a new Employee object
        employee = Employee.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            username=username,
            # If 'is_lead' is not provided, default to False
            is_lead=validated_data.get('is_lead', False)
        )

        # Set the password for the employee
        employee.set_password(validated_data['password'])
        # Save the employee object to the database
        employee.save()

        # Return the newly created employee object
        return employee
    