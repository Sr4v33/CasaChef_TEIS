# Entregable 2 — Microservicio Flask, APIs e Integraciones

Este archivo documenta únicamente la parte implementada para **Microservicio Flask, APIs e Integraciones**.

## 1. Decisión arquitectónica

Se agregó un microservicio Flask independiente llamado `casachef-recommendations-service`, ubicado en:

```text
microservices/recommendations/
```

La decisión evita tocar la lógica existente del monolito Django. Los módulos actuales de `dishes`, `orders`, `payments`, `cart`, `production` y `users` permanecen con sus rutas y responsabilidades originales.

## 2. Servicio Flask creado

El microservicio expone endpoints JSON bajo `/api/v2/`:

```text
GET /health/live
GET /health/ready
GET /api/v2/capabilities/
GET /api/v2/recommendations/
GET /api/v2/integrations/ally/menu/
GET /api/v2/integrations/third-party/country/<country_code>/
GET /api/v2/integrations/summary/
```

### Servicio a proveer

```text
GET /api/v2/capabilities/
GET /api/v2/recommendations/
```

Estos endpoints retornan información relevante del sistema CasaChef en JSON: capacidades del microservicio y recomendaciones filtrables por ciudad, presupuesto y tipo de comida.

## 3. Servicio a consumir: equipo aliado

El microservicio consume un servicio aliado usando el contrato:

```text
ALLY_SERVICE_BASE_URL=http://equipo-aliado:puerto
ALLY_MENU_ENDPOINT=/api/v1/public-menu/
```

Endpoint propio:

```text
GET /api/v2/integrations/ally/menu/?city=Medellin
```

Si el servicio aliado no está configurado o no responde, se entrega un fallback controlado en JSON. Esto permite sustentar la integración sin que una falla externa tumbe CasaChef.

## 4. API de terceros mediante Adapter

La API de terceros se consume a través de `RestCountriesAdapter`:

```text
microservices/recommendations/recommendations/infrastructure/adapters.py
```

El dominio no llama directamente a RestCountries. Solo conoce el contrato `CountryInfoPort`:

```text
microservices/recommendations/recommendations/domain/ports.py
```

Endpoint:

```text
GET /api/v2/integrations/third-party/country/CO/
```

Esto cumple inversión de dependencias: la lógica de aplicación depende de una abstracción y no del proveedor externo.

## 5. Integración Django ↔ Flask

Se agregó una app Django liviana:

```text
apps/integrations/
```

Rutas nuevas en Django:

```text
GET /api/integrations/
GET /api/integrations/microservice/health/
GET /api/integrations/capabilities/
GET /api/integrations/recommendations/
GET /api/integrations/ally-menu/
GET /api/integrations/country/<country_code>/
GET /api/integrations/summary/
```

Django consume Flask usando `RecommendationsMicroserviceClient`, ubicado en:

```text
apps/integrations/application/clients/microservice_client.py
```

La URL del microservicio se configura con:

```text
RECOMMENDATIONS_SERVICE_URL=http://127.0.0.1:5001
```

## 6. Comandos de prueba sugeridos

Terminal 1 — Django:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Terminal 2 — Flask:

```bash
cd microservices/recommendations
pip install -r requirements.txt
python app.py
```

Pruebas directas al microservicio Flask:

```bash
curl http://127.0.0.1:5001/health/ready
curl http://127.0.0.1:5001/api/v2/capabilities/
curl "http://127.0.0.1:5001/api/v2/recommendations/?city=Medellin&budget=30000"
curl "http://127.0.0.1:5001/api/v2/integrations/ally/menu/?city=Medellin"
curl http://127.0.0.1:5001/api/v2/integrations/third-party/country/CO/
curl "http://127.0.0.1:5001/api/v2/integrations/summary/?country=CO&city=Medellin"
```

Pruebas desde Django hacia Flask:

```bash
curl http://127.0.0.1:8000/api/integrations/
curl http://127.0.0.1:8000/api/integrations/microservice/health/
curl "http://127.0.0.1:8000/api/integrations/recommendations/?city=Medellin&budget=30000"
curl "http://127.0.0.1:8000/api/integrations/ally-menu/?city=Medellin"
curl http://127.0.0.1:8000/api/integrations/country/CO/
curl "http://127.0.0.1:8000/api/integrations/summary/?country=CO&city=Medellin"
```

## 7. Archivos modificados o agregados

Agregados:

```text
microservices/recommendations/
apps/integrations/
ENTREGABLE_2_MICROSERVICIO_APIS_INTEGRACIONES.md
```

Modificados:

```text
config/settings.py
config/urls.py
requirements.txt
env-ejemplo.txt
README.md
```

No se modificaron modelos, migraciones ni lógica de negocio existente de pedidos, pagos, producción, productos, carrito o usuarios.
