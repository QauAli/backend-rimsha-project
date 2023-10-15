from flask import Flask
from flask_smorest import Api
from resources.Staff import blp as StaffBlueprint
#from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores Rest API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["OPENAPI_VERSION"] = "3.0.3"  # Specify the OpenAPI version
app.config["JWT_SECRET_KEY"] = "8936237764654272374842989792124209905"

api = Api(app)
#jwt = JWTManager(app)
api.register_blueprint(StaffBlueprint)

if __name__ == '__main__':
    app.run()


