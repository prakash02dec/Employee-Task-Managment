# Import necessary modules from Django
from django.urls import path, include

# Import views from the current directory
from .views import employeeList , employeeDetail , assignTask

# Define the app name
app_name = "employees"

# Define the URL patterns for this app
urlpatterns = [
    # Path for listing all employees
    path("",  employeeList  ),
    
    # Path for retrieving, updating, or deleting a specific employee
    path("<int:id>", employeeDetail ),
    
    # Path for assigning a task to a specific employee
    path("<int:employeeID>/assignTask/<int:taskID>" , assignTask )
]