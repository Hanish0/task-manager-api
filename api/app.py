from flask import Flask
from api.routes import task_bp
from flasgger import Swagger
from api.auth_routes import auth_bp
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours =1)
jwt = JWTManager(app)

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
    },
     "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {"Bearer": []}
    ]
}
app.register_blueprint(task_bp)
app.register_blueprint(auth_bp)
swagger = Swagger(app,config=swagger_config, template=swagger_template)

@app.route('/')
def home():
    return {"message": "Welcome to Task Manager API!"}

if __name__ == '__main__':
    app.run(debug=True)