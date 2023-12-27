from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token

# Employee model that extends the built-in AbstractUser model
class Employee(AbstractUser):
    # Employee's name
    name = models.CharField(max_length=50)
    
    # Boolean field to check if the employee is a lead
    is_lead = models.BooleanField(default=False)
    
    # Employee's email, must be unique
    email = models.EmailField(unique=True)

    # Use email as the username field
    USERNAME_FIELD = 'email'
    
    # No other fields are required
    REQUIRED_FIELDS = []

    # Override the save method
    def save(self, *args, **kwargs):
        # Call the save method of the superclass
        super().save(*args, **kwargs)
        
        # Create a token for the user if it doesn't exist
        Token.objects.get_or_create(user=self)