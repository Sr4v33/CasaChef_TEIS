import logging
from config.celery import app

logger = logging.getLogger(__name__)

@app.task(bind=True, max_retries=3)
def send_order_notification(self, order_id: int, event: str):
    try:
        logger.info("[CELERY] Orden %s → %s", order_id, event)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)