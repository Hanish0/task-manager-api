# Task Manager API

A simple REST API for managing tasks built with Flask and MongoDB.

## Endpoints

- `GET /tasks` - Get all tasks
- `POST /tasks` - Create a new task
- `GET /tasks/<id>` - Get a specific task
- `PUT /tasks/<id>` - Update a task
- `DELETE /tasks/<id>` - Delete a task

## Documentation

API documentation is available at `/docs` once the server is running.

## Local Development

1. Install dependencies: `pip install -r requirements.txt`
2. Make sure MongoDB is running locally
3. Run the application: `python -m api.app`

