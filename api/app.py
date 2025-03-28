from flask import Flask
from api.routes import task_bp

app = Flask(__name__)

app.register_blueprint(task_bp)

@app.route('/')
def home():
    return {"message": "Welcome to Task Manager API!"}

if __name__ == '__main__':
    app.run(debug=True)