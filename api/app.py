from flask import Flask
from api.routes import task_bp
from flasgger import Swagger

app = Flask(__name__)

# configure swagger
swagger_config = {
    "headers" : [],
    "specs": [
        {
            "endpoint": "apispec",
            "route" : "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path":"/flasgger_static",
    "swagger_ui" : True,
    "specs_route" : "/docs/"
}

swagger_template = {
    "info": {
        "title": "Task Manager API",
        "description": "API for managing tasks",
        "version": "1.0.0"
    }
}
app.register_blueprint(task_bp)
swagger = Swagger(app,config=swagger_config, template=swagger_template)

@app.route('/')
def home():
    return {"message": "Welcome to Task Manager API!"}

if __name__ == '__main__':
    app.run(debug=True)