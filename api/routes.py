from flask import Blueprint, jsonify, request, make_response
from api.models import task_collection
from bson import ObjectId
from bson.errors import InvalidId
from marshmallow import Schema, fields, ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity


task_bp = Blueprint('task_bp', __name__)

class TaskSchema(Schema):
    title = fields.Str(required=True)
    status = fields.Str(required=True)

task_schema = TaskSchema()

def task_serializer(task):
    return {
        "id": str(task["_id"]),
        "title": task.get("title", "Untitled Task"),
        "status": task.get("status", "unknown"),
        "user": task.get("user", None)
    }

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """
    Create a new task
    ---
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Task
          required:
            - title
            - status
          properties:
            title:
              type: string
              description: The task title
            status:
              type: string
              description: The task status
    responses:
      201:
        description: Task created successfully
      400:
        description: Invalid input data
      401:
        description: Missing or invalid token
    """
    try:
        current_user = get_jwt_identity()
        data = request.json
        if not data:
            return jsonify({"error": "No data"}), 400
        errors = task_schema.validate(data)
        if errors:
            return jsonify({"error": "Validation error", "details": errors}), 400

        # Add the user to the task
        data['user'] = current_user
        
        task_id = task_collection.insert_one(data).inserted_id
        return jsonify({"message": "Task created", "id": str(task_id)}), 201
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}),500

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """
    Get all tasks for the authenticated user
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: A list of tasks
      401:
        description: Missing or invalid token
    """
    try:
        current_user = get_jwt_identity()
        tasks = list(task_collection.find({"user": current_user}))
        return jsonify([task_serializer(task) for task in tasks]), 200
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500

@task_bp.route('/tasks/<id>', methods=['GET'])
@jwt_required()
def get_task(id):
    """
    Get a specific task by ID
    ---
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The task ID
    responses:
      200:
        description: Task found
      400:
        description: Invalid task ID format
      401:
        description: Missing or invalid token
      403:
        description: Access denied
      404:
        description: Task not found
    """
    try:
        current_user = get_jwt_identity()
        task = task_collection.find_one({"_id": ObjectId(id)})
        
        if not task:
            return jsonify({"error": "Task not found"}), 404
            
        # Check if the task belongs to the current user
        if task.get('user') != current_user:
            return jsonify({"error": "Access denied"}), 403
            
        return jsonify(task_serializer(task)), 200
    except InvalidId:
        return jsonify({"error": "Invalid task ID format"}), 400
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500


@task_bp.route('/tasks/<id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    """
    Update a task by ID
    ---
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The task ID
      - in: body
        name: body
        required: true
        schema:
          id: TaskUpdate
          properties:
            title:
              type: string
              description: The new task title
            status:
              type: string
              description: The new task status
    responses:
      200:
        description: Task updated successfully
      400:
        description: Invalid input data or ID
      401:
        description: Missing or invalid token
      403:
        description: Access denied
      404:
        description: Task not found
    """

    try:
        current_user = get_jwt_identity()
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # First check if the task exists and belongs to the user
        task = task_collection.find_one({"_id": ObjectId(id)})
        if not task:
            return jsonify({"error": "Task not found"}), 404
            
        if task.get('user') != current_user:
            return jsonify({"error": "Access denied"}), 403
            
        # Don't allow changing the user
        if 'user' in data:
            del data['user']
            
        result = task_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.modified_count > 0:
            return jsonify({"message": "Task updated"}), 200
        else:
            return jsonify({"message": "No changes made to task"}), 200
    except InvalidId:
        return jsonify({"error": "Invalid task ID format"}), 400
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}) ,500


@task_bp.route('/tasks/<id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    """
    Delete a task by ID
    ---
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The task ID
    responses:
      200:
        description: Task deleted successfully
      400:
        description: Invalid task ID format
      401:
        description: Missing or invalid token
      403:
        description: Access denied
      404:
        description: Task not found
    """
    try:
        current_user = get_jwt_identity()
        
        # First check if the task exists and belongs to the user
        task = task_collection.find_one({"_id": ObjectId(id)})
        if not task:
            return jsonify({"error": "Task not found"}), 404
            
        if task.get('user') != current_user:
            return jsonify({"error": "Access denied"}), 403
        
        result = task_collection.delete_one({"_id": ObjectId(id)})
        return jsonify({"message": "Task deleted"}), 200
    except InvalidId:
        return jsonify({"error": "Invalid task ID format"}), 400
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500