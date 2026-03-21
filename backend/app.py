from flask import Flask, jsonify, request
from flask_cors import CORS
from pydantic import ValidationError

from models.comps_model import CompsModel
from models.dcf_model import DcfModel
from models.exceptions import NoCompsFoundError, InsufficientDataError, CalculationError
from models.valuation_model import ValuationModel
from schemas.request import ValuationRequest, Sector, ModelType

# Production default registry — one instance per model type
MODEL_REGISTRY: dict[ModelType, ValuationModel] = {
    ModelType.COMPS: CompsModel(),
    ModelType.DCF: DcfModel(),
}


def create_app(registry: dict[ModelType, ValuationModel] = None) -> Flask:
    if registry is None:
        registry = MODEL_REGISTRY  # use production default

    app = Flask(__name__)
    CORS(app)

    @app.route("/api/models", methods=["GET"])
    def get_models():
        return jsonify([m.value for m in ModelType])

    @app.route("/api/sectors", methods=["GET"])
    def get_sectors():
        return jsonify([s.value for s in Sector])

    @app.route("/api/valuate", methods=["POST"])
    def valuate():
        try:
            valuation_request = ValuationRequest(**request.get_json(force=True))
        except (ValidationError, TypeError) as e:
            return jsonify({"error": "ValidationError", "message": str(e), "status": 400}), 400

        try:
            report = registry[valuation_request.model].run(valuation_request)
            return jsonify(report.model_dump()), 200
        except (NoCompsFoundError, InsufficientDataError) as e:
            return jsonify({"error": type(e).__name__, "message": str(e), "status": 422}), 422
        except CalculationError as e:
            return jsonify({"error": "CalculationError", "message": str(e), "status": 500}), 500
        except Exception as e:
            return jsonify({"error": "InternalError", "message": str(e), "status": 500}), 500

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
