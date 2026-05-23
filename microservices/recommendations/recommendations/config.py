import os


class Settings:
    """Configuración del microservicio.

    Se mantiene separada para evitar textos/URLs quemadas dentro de la lógica de
    negocio y facilitar despliegue local, Docker o AWS.
    """

    SERVICE_NAME = "casachef-recommendations-service"
    SERVICE_VERSION = "2.0.0"
    ALLY_SERVICE_BASE_URL = os.getenv("ALLY_SERVICE_BASE_URL", "").rstrip("/")
    ALLY_MENU_ENDPOINT = os.getenv("ALLY_MENU_ENDPOINT", "/api/v1/public-menu/")
    THIRD_PARTY_COUNTRY_API = os.getenv(
        "THIRD_PARTY_COUNTRY_API",
        "https://restcountries.com/v3.1/alpha",
    ).rstrip("/")
    REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "3"))
