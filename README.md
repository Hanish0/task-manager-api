# Task Manager API

A secure REST API for managing tasks built with Flask, MongoDB, and JWT authentication.

## Features

- User authentication with JWT
- Task management with proper user ownership
- RESTful API design
- Swagger documentation
- MongoDB integration

## Authentication Endpoints

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token
- `GET /auth/protected` - Test authenticated access

## Task Endpoints

- `GET /tasks` - Get all tasks for the authenticated user
- `POST /tasks` - Create a new task
- `GET /tasks/<id>` - Get a specific task
- `PUT /tasks/<id>` - Update a task
- `DELETE /tasks/<id>` - Delete a task

## Documentation

API documentation is available at `/docs` once the server is running.

## Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file from `.env.sample`:
   ```
   MONGODB_URI=mongodb://localhost:27017/
   DB_NAME=taskdb
   JWT_SECRET_KEY=your-secure-secret-key-here
   ```
6. Make sure MongoDB is running locally
7. Run the application: `python -m api.app`

## Testing the API with cURL

### User Registration

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "securepassword123"}'
```

### User Login

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "securepassword123"}'
```

This returns a JWT token that you'll use for subsequent requests:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Creating a Task

```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"title": "My First Task", "status": "pending"}'
```

### Getting All Tasks

```bash
curl -X GET http://localhost:5000/tasks \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Testing with Postman

### Setting Up Postman

1. Download and install [Postman](https://www.postman.com/downloads/)
2. Create a new collection for Task Manager API
3. Set up environment variables for easier testing:
   - Click on the "Environments" tab
   - Create a new environment called "Task Manager API"
   - Add these variables:
     - `base_url`: `http://localhost:5000`
     - `token`: Leave this empty (will be populated after login)

### User Registration in Postman

1. Create a new request:
   - Method: `POST`
   - URL: `{{base_url}}/auth/register`
   - Headers: Add `Content-Type: application/json`
   - Body: Select "raw" and choose "JSON", then enter:
     ```json
     {
       "username": "testuser",
       "password": "securepassword123"
     }
     ```
2. Send the request to register the user

### User Login in Postman

1. Create a new request:
   - Method: `POST`
   - URL: `{{base_url}}/auth/login`
   - Headers: Add `Content-Type: application/json`
   - Body: Select "raw" and choose "JSON", then enter:
     ```json
     {
       "username": "testuser",
       "password": "securepassword123"
     }
     ```
2. Send the request to get your JWT token
3. To save the token automatically, go to the Tests tab and add:
   ```javascript
   var jsonData = pm.response.json();
   pm.environment.set("token", jsonData.access_token);
   ```

### Creating a Task in Postman

1. Create a new request:
   - Method: `POST`
   - URL: `{{base_url}}/tasks`
   - Headers: 
     - `Content-Type: application/json`
     - `Authorization: Bearer {{token}}`
   - Body: Select "raw" and choose "JSON", then enter:
     ```json
     {
       "title": "My First Task",
       "status": "pending"
     }
     ```
2. Send the request to create a task

### Getting All Tasks in Postman

1. Create a new request:
   - Method: `GET`
   - URL: `{{base_url}}/tasks`
   - Headers: `Authorization: Bearer {{token}}`
2. Send the request to retrieve all your tasks

### Getting a Single Task in Postman

1. Create a new request:
   - Method: `GET`
   - URL: `{{base_url}}/tasks/YOUR_TASK_ID`
   - Headers: `Authorization: Bearer {{token}}`
2. Send the request to retrieve the specific task

### Updating a Task in Postman

1. Create a new request:
   - Method: `PUT`
   - URL: `{{base_url}}/tasks/YOUR_TASK_ID`
   - Headers: 
     - `Content-Type: application/json`
     - `Authorization: Bearer {{token}}`
   - Body: Select "raw" and choose "JSON", then enter:
     ```json
     {
       "title": "Updated Task",
       "status": "completed"
     }
     ```
2. Send the request to update the task

### Deleting a Task in Postman

1. Create a new request:
   - Method: `DELETE`
   - URL: `{{base_url}}/tasks/YOUR_TASK_ID`
   - Headers: `Authorization: Bearer {{token}}`
2. Send the request to delete the task

## Security Notes

- Use a strong, unique secret key for JWT in production
- Never commit the `.env` file with secrets to version control
- Always use HTTPS in production environments
- JWT tokens expire after 1 hour by default; configure as needed

## Dependencies

- Flask - Web framework
- PyMongo - MongoDB integration
- Flask-JWT-Extended - JWT authentication
- Flasgger - API documentation
- Marshmallow - Schema validation
- Passlib - Password hashing
- Python-dotenv - Environment configuration