# Import necessary modules and classes
from .models import Employee
from .serializers import EmployeeSerializer , EmployeeListSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from tasks.models import Task
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


# View for logging out a user
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only authenticated users can access this view
def logout(request):
    # Delete the user's authentication token
    request.user.auth_token.delete()
    # Return a 200 OK response
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    # Get the email and password from the request data
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Authenticate the user
    user = authenticate(request, username=email, password=password)
    
    # If the user is not authenticated, return an error response
    if user is None:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get or create a token for the user
    token, created = Token.objects.get_or_create(user=user)
    
    # Return the token in the response
    return Response({'token': token.key}, status=status.HTTP_200_OK)


# View for listing all employees or creating a new employee
@api_view(['GET', 'POST'])
def employeeList(request):
    # If the request method is GET, list all employees
    if request.method == 'GET':
        # Get all Employee objects
        employees = Employee.objects.all()
        # Serialize the employees
        serializer = EmployeeListSerializer(employees, many=True)
        # Return the serialized employees
        return Response(serializer.data , status=status.HTTP_200_OK)

    # If the request method is POST, create a new employee
    if request.method == 'POST':
        # Serialize the request data
        serializer = EmployeeSerializer(data=request.data)
        # If the serialized data is valid, save it as a new Employee object
        if (serializer.is_valid()):
            serializer.save()
            # Return the serialized data of the new employee
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If the serialized data is not valid, return an error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for retrieving, updating, or deleting a specific employee
@api_view(['GET' , 'PUT' , 'DELETE'])
def employeeDetail(request , id):
    # Try to get the Employee object with the given id
    try:
        employee = Employee.objects.get(pk=id)
    # If the Employee object does not exist, return an error
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # If the request method is GET, retrieve the employee
    if request.method == 'GET':
        # Serialize the employee
        serializer = EmployeeListSerializer(employee)
        # Return the serialized employee
        return Response(serializer.data , status=status.HTTP_200_OK)

    # If the request method is PUT, update the employee
    if request.method == 'PUT':
        # Serialize the request data and the existing employee
        serializer = EmployeeListSerializer(employee , data=request.data)
        # If the serialized data is valid, save it as the updated Employee object
        if (serializer.is_valid()):
            serializer.save()
            # Return the serialized data of the updated employee
            return Response(serializer.data , status=status.HTTP_200_OK)
        # If the serialized data is not valid, return an error
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    # If the request method is DELETE, delete the employee
    if request.method == 'DELETE':
        # Delete the employee
        employee.delete()
        # Return a 204 No Content response
        return Response(status=status.HTTP_204_NO_CONTENT)


# View for assigning a task to a specific employee
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only authenticated users can access this view
def assignTask(request , employeeID , taskID):
    # Try to get the Employee and Task objects with the given ids
    try:
        employee = Employee.objects.get(id=employeeID)
        task = Task.objects.get(id=taskID)
    # If the Employee or Task object does not exist, return an error
    except (Employee.DoesNotExist, Task.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Check if the user making the request is a lead
    if not request.user.is_lead:
        return Response({'detail': 'Only leads can assign tasks.'}, status=status.HTTP_403_FORBIDDEN)

    # Check if the employee being assigned the task is a lead
    if employee.is_lead:
        return Response({'detail': 'Leads cannot be assigned tasks.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the task is already assigned to the employee
    if task.assignee == employee:
        return Response({'detail': 'This task is already assigned to the employee.'}, status=status.HTTP_400_BAD_REQUEST)

    # Assign the task to the employee
    task.assignee = employee
    # Save the updated task
    task.save()
    # Serialize the updated employee
    serialize = EmployeeSerializer(Employee.objects.get(id=employeeID))
    # Return the serialized updated employee
    return Response(serialize.data ,status=status.HTTP_200_OK)