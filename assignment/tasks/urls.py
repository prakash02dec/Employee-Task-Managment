# Import necessary modules from Django
from django.urls import path, include

# Import views from the current directory
from .views import TaskList, TaskDetail

# Define the app name
app_name = "tasks"

# Define the URL patterns for this app
urlpatterns = [
    # Path for listing all tasks
    path("", TaskList),
    
    # Path for retrieving, updating, or deleting a specific task
    path("<int:id>", TaskDetail)
]