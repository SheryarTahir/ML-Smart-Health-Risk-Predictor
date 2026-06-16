"""Smart Health Risk Predictor — Flask entry point."""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config.config import Config
from routes.auth import auth_bp
from routes.predict import predict_bp
from routes.history import history_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "*"}})
    JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix="")
    app.register_blueprint(predict_bp, url_prefix="/predict")
    app.register_blueprint(history_bp, url_prefix="")

    @app.get("/")
    def root():
        return jsonify(
            name="Smart Health Risk Predictor API",
            version="1.0.0",
            endpoints=[
                "POST /register", "POST /login",
                "POST /predict/heart", "POST /predict/diabetes",
                "POST /predict/obesity",
                "GET /history", "GET /reports",
            ],
        )

    @app.errorhandler(404)
    def not_found(_):
        return jsonify(error="Not found"), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify(error="Internal server error", detail=str(e)), 500

    return app



if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5002, debug=True)
