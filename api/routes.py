from flask import Blueprint, jsonify, request
from api.models import task_collection
from bson import ObjectId

task_bp = Blueprint('task_bp', __name__)

def task_serializer(task):
    return {
        "id": str(task["_id"]),
        "title": task.get("title", "Untitled Task"),  # Use "title" instead of "task"
        "status": task.get("status", "unknown")  # Avoid KeyError
    }

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    
    data = request.json
    if not data or "title" not in data or "status" not in data:
        return jsonify({"error": "Missing required fields: title, status"}), 400

    task_id = task_collection.insert_one(data).inserted_id
    return jsonify({"message": "Task created", "id": str(task_id)}), 201


@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = list(task_collection.find())  # Convert cursor to list
    return jsonify([task_serializer(task) for task in tasks]), 200

@task_bp.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    try:
        task = task_collection.find_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "Invalid task ID format"}), 400

    if task:
        return jsonify(task_serializer(task)), 200
    return jsonify({"error": "Task not found"}), 404

@task_bp.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    data = request.json
    try:
        result = task_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    except:
        return jsonify({"error": "Invalid task ID format"}), 400

    if result.modified_count > 0:
        return jsonify({"message": "Task updated"}), 200
    return jsonify({"error": "Task not found or no changes"}), 404

@task_bp.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    try:
        result = task_collection.delete_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "Invalid task ID format"}), 400

    if result.deleted_count > 0:
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404
