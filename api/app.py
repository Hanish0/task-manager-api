from flask import Flask
from api.models import task_collection

app = Flask(__name__)

@app.route('/')
def home():
    return {"message": "Welcome to Task Manager API!"}

@app.route('/test-db')
def test_db():
    test_task = {"title": "Test task", "status": "pending"}
    result = task_collection.insert_one(test_task)
    return {"message": "task inserted", "id": str(result.inserted_id)}


if __name__ == '__main__':
    app.run(debug=True)