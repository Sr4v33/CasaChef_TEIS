from __future__ import annotations

from typing import Optional

from flask import Blueprint, current_app, jsonify, request

from recommendations.application.services import IntegrationFacade, RecommendationService
from recommendations.infrastructure.adapters import AllyMenuHttpClient, RestCountriesAdapter

api_bp = Blueprint("recommendations_api", __name__)


def _parse_float(value: Optional[str]) -> Optional[float]:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError("budget debe ser numérico") from exc


def _parse_int(value: Optional[str], default: int) -> int:
    if value in (None, ""):
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError("limit debe ser entero") from exc


def _build_recommendation_service() -> RecommendationService:
    return RecommendationService()


def _build_facade() -> IntegrationFacade:
    timeout = current_app.config["REQUEST_TIMEOUT_SECONDS"]
    recommendation_service = _build_recommendation_service()
    country_adapter = RestCountriesAdapter(
        base_url=current_app.config["THIRD_PARTY_COUNTRY_API"],
        timeout_seconds=timeout,
    )
    ally_client = AllyMenuHttpClient(
        base_url=current_app.config["ALLY_SERVICE_BASE_URL"],
        endpoint=current_app.config["ALLY_MENU_ENDPOINT"],
        timeout_seconds=timeout,
    )
    return IntegrationFacade(
        recommendation_service=recommendation_service,
        country_info=country_adapter,
        ally_menu=ally_client,
    )


@api_bp.get("/health/live")
def health_live():
    return jsonify({"status": "alive", "service": current_app.config["SERVICE_NAME"]}), 200


@api_bp.get("/health/ready")
def health_ready():
    return jsonify(
        {
            "status": "ready",
            "service": current_app.config["SERVICE_NAME"],
            "version": current_app.config["SERVICE_VERSION"],
            "ally_configured": bool(current_app.config["ALLY_SERVICE_BASE_URL"]),
        }
    ), 200


@api_bp.get("/api/v2/capabilities/")
def capabilities():
    return jsonify(_build_recommendation_service().capabilities()), 200


@api_bp.get("/api/v2/recommendations/")
def recommendations():
    service = _build_recommendation_service()
    payload = service.build_recommendations(
        city=request.args.get("city"),
        budget=_parse_float(request.args.get("budget")),
        dish_type=request.args.get("dish_type"),
        limit=_parse_int(request.args.get("limit"), default=3),
    )
    return jsonify(payload), 200


@api_bp.get("/api/v2/integrations/ally/menu/")
def ally_menu():
    facade = _build_facade()
    return jsonify(facade.ally_menu(city=request.args.get("city"))), 200


@api_bp.get("/api/v2/integrations/third-party/country/<country_code>/")
def country_context(country_code: str):
    facade = _build_facade()
    return jsonify(facade.country_context(country_code)), 200


@api_bp.get("/api/v2/integrations/summary/")
def integration_summary():
    facade = _build_facade()
    payload = facade.integrated_summary(
        country_code=request.args.get("country", "CO"),
        city=request.args.get("city"),
        budget=_parse_float(request.args.get("budget")),
        dish_type=request.args.get("dish_type"),
    )
    return jsonify(payload), 200


def register_error_handlers(app):
    @app.errorhandler(ValueError)
    def handle_value_error(exc):
        return jsonify({"error": str(exc)}), 400

    @app.errorhandler(404)
    def handle_not_found(exc):
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(Exception)
    def handle_unexpected_error(exc):
        app.logger.exception("Unhandled microservice error")
        return jsonify({"error": "Error interno del microservicio"}), 500
