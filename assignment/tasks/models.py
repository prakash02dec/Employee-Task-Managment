from django.db import models


# Task model
class Task(models.Model):
    # Title of the task, a CharField with a maximum length of 50 characters
    title = models.CharField(max_length=50)
    
    # Description of the task, a TextField
    description = models.TextField()
    
    # Deadline of the task, a DateTimeField
    deadline = models.DateTimeField()
    
    # Employee assigned to the task, a ForeignKey to the Employee model
    # If the related Employee is deleted, the assignee field is set to NULL
    assignee = models.ForeignKey('employees.Employee',related_name = 'tasks', on_delete=models.SET_NULL , null=True)
    
    # String representation of the Task model
    # Returns the title of the task
    def __str__(self):
        return self.title