# basic documentation for assignment

## Overview

This API allows for the management of employees and tasks within an organization. It supports operations such as creating, retrieving, updating, and deleting employees and tasks.

## Authentication

Task assignment and logout API require authenticaton. Token will be generated once you login. To authenticate, include the token in the `Authorization` header with the user `Token` keyword:  
Authorization: Token token_here

## Endpoints

### `/api/employees/`

- `GET`: Retrieve a list of all employees.
- `POST`: Create a new employee. Requires `name`, `email`, and `password` fields. The `is_lead` field is optional.
    

### `/api/employees/`

- `GET`: Retrieve the details of the employee with the given ID.
- `PUT`: Update the details of the employee with the given ID. Does not allow updating the `email` field.
- `DELETE`: Delete the employee with the given ID.
    

### `/api/tasks/`

- `GET`: Retrieve a list of all tasks.
- `POST`: Create a new task. Requires `title` and `description` fields.
    

### `/api/tasks/`

- `GET`: Retrieve the details of the task with the given ID.
- `PUT`: Update the details of the task with the given ID.
- `DELETE`: Delete the task with the given ID.
    

### `/api/tasks/assign/`

- `POST`: Assign the task with the given ID to the employee with the given ID. Only leads can assign tasks, and they cannot assign tasks to other leads.