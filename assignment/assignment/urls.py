from django.contrib import admin
from django.urls import path, include
from employees.views import login, logout


urlpatterns = [
    # Django admin interface
    path("admin/", admin.site.urls),
    
    # Include the URLs from the 'employees' app
    path("employees/", include("employees.urls" , namespace = "employees")),
    
    # Include the URLs from the 'tasks' app
    path("tasks/", include("tasks.urls" , namespace = "tasks")),
    
    # Login view
    path('login/', login, name='login'),
    
    # Logout view
    path('logout/', logout, name='logout'),
]