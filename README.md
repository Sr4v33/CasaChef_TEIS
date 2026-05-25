# CasaChef

CasaChef es una plataforma para gestionar platos caseros bajo pedido con foco en producción diaria, control de cupos y trazabilidad del ciclo de vida de cada orden.

## Qué incluye este proyecto

- Gestión de productos, producción, pedidos, pagos, usuarios y carrito.
- Reserva de cupos de producción en transacciones atómicas al crear pedidos.
- Procesos asíncronos con Celery + Redis para notificaciones y reporte diario de pedidos.
- Soporte bilingüe `es/en` con Django i18n y selector de idioma en la interfaz.
- Panel web único para catálogo, creación de pedidos, consulta y producción.

## Stack principal

- Django 5
- Django REST Framework
- Celery 5
- Redis 7
- SQLite
- Docker Compose

## Variables de entorno

Usa `env-ejemplo.txt` como base para crear `.env`.

Variables relevantes:

- `DEBUG=True`
- `SECRET_KEY=...`
- `PAYMENT_PROVIDER=MOCK`
- `ENV_TYPE=DEV`
- `NOTIFIER=CONSOLE`
- `REDIS_URL=redis://redis:6379/0`
- `RECOMMENDATIONS_SERVICE_URL=http://127.0.0.1:5001`
- `INTEGRATION_HTTP_TIMEOUT=3`

`NOTIFIER` acepta `CONSOLE` o `EMAIL`. Si no se define, el proyecto cae en `ENV_TYPE` para decidir el notifier.

## Levantar con Docker

1. Crea `.env` en la raíz del proyecto.
2. Ejecuta:

```bash
docker compose up --build
```

Servicios levantados:

- `django`: aplicación principal
- `celery`: worker asíncrono
- `redis`: broker y backend de resultados
- `recommendations`: microservicio de recomendaciones
- `nginx`: entrada pública

## Ejecución local

La ruta recomendada para desarrollo completo es Docker, porque levanta Django, Redis, Celery y el microservicio juntos.

Si quieres correr partes por separado:

```bash
python manage.py migrate
python manage.py runserver
celery -A config worker -l info --concurrency=2
```

## Internacionalización

La app usa `LocaleMiddleware`, selector de idioma y archivos de traducción bajo `locale/en/LC_MESSAGES/`.

Para compilar traducciones en Windows sin depender de `django-admin compilemessages`, se añadió:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\compile_translations.ps1
```

Esto genera:

- `locale/en/LC_MESSAGES/django.mo`
- `locale/en/LC_MESSAGES/djangojs.mo`

## Procesos asíncronos

Celery se usa para:

- Notificaciones de pedidos `CREATED`, `CONFIRMED` y `CANCELLED`
- Actualización de un reporte diario agregado por fecha de entrega

Las tareas están en:

- `apps/orders/infrastructure/tasks/notification_tasks.py`

## Ruta principal

- Panel web: `http://127.0.0.1:8000/`
- Admin Django: `http://127.0.0.1:8000/admin/`
- API root: `http://127.0.0.1:8000/api/`
