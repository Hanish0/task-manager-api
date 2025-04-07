from flask import Blueprint, jsonify, request, make_response
from api.models import task_collection
from bson import ObjectId
from bson.errors import InvalidId
from marshmallow import Schema, fields, ValidationError


task_bp = Blueprint('task_bp', __name__)

class TaskSchema(Schema):
    title = fields.Str(required=True)
    status = fields.Str(required=True)

task_schema = TaskSchema()

def task_serializer(task):
    return {
        "id": str(task["_id"]),
        "title": task.get("title", "Untitled Task"),
        "status": task.get("status", "unknown")
    }

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    Create a new task
    ---
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
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data"}), 400
        errors = task_schema.validate(data)
        if errors:
            return jsonify({"error": "Validation error", "details": errors}), 400

        task_id = task_collection.insert_one(data).inserted_id
        return jsonify({"message": "Task created", "id": str(task_id)}), 201
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}),500

@task_bp.route('/tasks', methods=['GET'])

def get_tasks():
    """
    Get all tasks
    ---
    responses:
      200:
        description: A list of tasks
    """
    try:
        tasks = list(task_collection.find())
        return jsonify([task_serializer(task) for task in tasks]), 200
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500

@task_bp.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    """
    Get a specific task by ID
    ---
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
      404:
        description: Task not found
    """
    try:
        task = task_collection.find_one({"_id": ObjectId(id)})
        if task:
            return jsonify(task_serializer(task)),200
        return jsonify({"error": "Task not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid task ID format"}), 400
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500


@task_bp.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    """
    Update a task by ID
    ---
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
      404:
        description: Task not found
    """

    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        result = task_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.modified_count > 0:
            return jsonify({"message": "Task updated"}), 200
        elif result.matched_count > 0:
            return jsonify({"message": "No changes made to task"}), 200
        return jsonify({"error": "Task not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid task ID format"}), 400
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}) ,500


@task_bp.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    """
    Delete a task by ID
    ---
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
      404:
        description: Task not found
    """
    try:
        result = task_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return jsonify({"message": "Task deleted"}), 200
        return jsonify({"error": "Task not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid task ID format"}), 400
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500


