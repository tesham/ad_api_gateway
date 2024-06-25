## Django REST API Gateway
This project implements a RESTful API using Django and Django REST Framework (DRF) for routing user request to appropriate microservice 

## Features

- Act as gateway, Routing path to corresponding microservice
- if path contains auth: it routes to auth microservice
- if path contains ip: it routes to ip microservice
- if path contains audit: it routes to audit microservice

### Prerequisites

- Python 3.9
- PostgreSQL
- Django 4.1.0
- Django REST Framework 3.14

### Installation

1. clone the repository

2. Create and activate a virtual environment if it doesn't exist in the project folder:
```
    python -m venv venv
    source venv/bin/activate
```

3. Install all the requirements using `pip`:
```
    pip install -r requirements.txt
```

6. Add these url as per running port in settings.py
```
    AUTH_SERVICE = 'http://127.0.0.1:8001'
    IP_SERVICE = 'http://127.0.0.1:8002'
    AUDIT_SERVICE = 'http://127.0.0.1:8003'
```
    
7. Start the server:
```
    python manage.py runserver
```


### Configuration

Update the `settings.py` file with your configurations. Ensure you have the `SECRET_KEY` and other necessary configurations set.

### Usage

#### Endpoints

- **User Registration:**
- Create user to access

    ```http
    POST /api/register/
    ```

    Request body:
    ```json
    {
        "username": "yourusername",
        "password": "yourpassword",
        "email": "youremail@example.com"
    }
    ```
  
    Response:
    ```json
    {
      "is_error": 0,
      "message": "success"
    }
    ```

- **User Login:**
- Only one active session will be preserved. If user has an active session and login api is called then user is denied to get token. User can get token again after successful logout

    ```http
    POST /api/auth/token/
    ```

    Request body:
    ```json
    {
        "username": "yourusername",
        "password": "yourpassword"
    }
    ```

    Response:
    ```json
    {
        "access_token": "youraccesstoken",
        "refresh_token": "yourrefreshtoken"
    }
    ```

- **Refresh Token:**

    ```http
    POST /api/auth/token/refresh/
    ```

    Request body:
    ```json
    {
        "refresh_token": "yourrefreshtoken"
    }
    ```

    Response:
    ```json
    {
        "access_token": "newaccesstoken"
    }
    ```

- **Logout (Blacklist Refresh Token):**

    ```http
    POST /api/auth/logout/
    ```

    Request body:
    ```json
    {
        "refresh_token": "yourrefreshtoken"
    }
    ```

    Response:
    ```json
    {
        "message": "Successfully logged out."
    }
    ```
  
- **IP View :**

    ```http
    GET /api/ip
    ```

    Response:
    ```json
  [
    {
        "id": 1,
        "ip": "223",
        "create_time": "2024-06-24T01:07:37.818314",
        "update_time": "2024-06-24T01:14:21.734781",
        "label": "test_t",
        "created_by": "223"
    }
  ]
  ```
    
- **IP Create:**

    ```http
    POST /api/ip
    ```

    Request body:
    ```json
    {
     "ip":"130.32.4.1",
     "label":"test_ip"
    }
    ```

    Response:
    ```json
    {
      "is_error": 0,
      "message": "success"
    }
    ```
  
- **IP Update:**

    ```http
    PUT /api/ip
    ```

    Request body:
    ```json
    {
     "id":1,
     "label":"test_update"
    }
    ```

    Response:
    ```json
    {
      "is_error": 0,
      "message": "success"
    }
    ```
  
- **Audit View:**

    ```http
    GET /api/audit?ip&module&user&label&start_date&end_date
    ```
    Query param:
    ```
      user : user_name like: admin or admin@gmail.com
      ip : ip address filter
      start date, end date : date range
      module : AUTH/IP
      label : Login/Logout, Create/Update
    ```    

    Response:
    ```json
    [
    {
        "id": 7,
        "user": "tesham29@gmail.com",
        "session_id": 21,
        "module": "AUTH",
        "label": "Login",
        "ip": null,
        "action": "user logged in  : tesham29@gmail.com",
        "created_at": "2024-06-24T17:57:31.747696"
    },
    {
        "id": 8,
        "user": "tesham29@gmail.com",
        "session_id": 21,
        "module": "AUTH",
        "label": "Logout",
        "ip": null,
        "action": "user logged out  : tesham29@gmail.com",
        "created_at": "2024-06-24T17:58:11.079064"
    }
    ]
    ```
