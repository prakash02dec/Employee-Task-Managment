# Import necessary modules and classes
from .serializers import TaskSerializer
from .models import Task
from rest_framework import status 
from rest_framework.decorators import api_view
from rest_framework.response import Response

# View for listing all tasks or creating a new task
@api_view(['GET' , 'POST'])
def TaskList(request):
    # If the request method is GET, list all tasks
    if(request.method == 'GET'):
        # Get all Task objects
        tasks = Task.objects.all()
        # Serialize the tasks
        serializer = TaskSerializer(tasks , many=True)
        # Return the serialized tasks
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    # If the request method is POST, create a new task
    if(request.method == 'POST'):
        # Serialize the request data
        serializer = TaskSerializer(data = request.data)
        # If the serialized data is valid, save it as a new Task object
        if(serializer.is_valid()):
            serializer.save()
            # Return the serialized data of the new task
            return Response(serializer.data , status = status.HTTP_201_CREATED)
        # If the serialized data is not valid, return an error
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
    

# View for retrieving, updating, or deleting a specific task
@api_view(['GET' , 'PUT' , 'DELETE'])
def TaskDetail(request , id):
    # Try to get the Task object with the given id
    try:
        task = Task.objects.get(pk = id)
    # If the Task object does not exist, return an error
    except Task.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    # If the request method is GET, retrieve the task
    if(request.method == 'GET'):
        # Serialize the task
        serializer = TaskSerializer(task)
        # Return the serialized task
        return Response(serializer.data , status = status.HTTP_200_OK)
    
    # If the request method is PUT, update the task
    elif(request.method == 'PUT'):
        # Serialize the request data and the existing task
        serializer = TaskSerializer(task , data = request.data)
        # If the serialized data is valid, save it as the updated Task object
        if(serializer.is_valid()):
            serializer.save() 
            # Return the serialized data of the updated task
            return Response(serializer.data , status = status.HTTP_200_OK)
        # If the serialized data is not valid, return an error
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
    
    # If the request method is DELETE, delete the task
    elif(request.method == 'DELETE'):
        # Delete the task
        task.delete()
        # Return a 204 No Content response
        return Response(status = status.HTTP_204_NO_CONTENT)
    


