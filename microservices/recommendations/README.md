# Microservicio Flask: Recommendations & Integrations

Este microservicio implementa la parte **Microservicio Flask, APIs e Integraciones** del Entregable 2 sin modificar el flujo principal del monolito Django.

## Responsabilidades

- Expone un endpoint JSON propio con capacidades y recomendaciones de CasaChef.
- Consume un servicio aliado configurable mediante variable de entorno.
- Consume una API de terceros mediante un Adapter, respetando inversión de dependencias.
- Responde siempre en JSON y tiene `health checks` para ejecución local, Docker y AWS.

## Ejecución local

```bash
cd microservices/recommendations
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py
```

Servicio disponible en:

```text
http://127.0.0.1:5001
```

## Variables de entorno

```text
ALLY_SERVICE_BASE_URL=http://equipo-aliado:8000
ALLY_MENU_ENDPOINT=/api/v1/public-menu/
THIRD_PARTY_COUNTRY_API=https://restcountries.com/v3.1/alpha
REQUEST_TIMEOUT_SECONDS=3
```

Si `ALLY_SERVICE_BASE_URL` no está configurado o el servicio aliado no responde, el microservicio entrega un fallback controlado para no romper la integración.

## Endpoints principales

```text
GET /health/live
GET /health/ready
GET /api/v2/capabilities/
GET /api/v2/recommendations/?city=Medellin&budget=30000&dish_type=almuerzo
GET /api/v2/integrations/ally/menu/
GET /api/v2/integrations/third-party/country/CO/
GET /api/v2/integrations/summary/?country=CO&city=Medellin
```

## Docker

```bash
docker build -t casachef-recommendations:latest .
docker run --rm -p 5001:5001 casachef-recommendations:latest
```
