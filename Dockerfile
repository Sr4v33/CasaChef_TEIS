FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends gettext && \
    python manage.py compilemessages --ignore=.venv --ignore=microservices && \
    apt-get purge -y gettext && \
    rm -rf /var/lib/apt/lists/*
EXPOSE 8000
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "config.wsgi:application"]