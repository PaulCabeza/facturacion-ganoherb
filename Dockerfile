# Use Python 3.11 slim image específicamente
FROM python:3.11.7-slim

# Desactivar mise explícitamente
ENV MISE_DISABLE=1
ENV MISE_PYTHON_DEFAULT_PACKAGES_FILE=""

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create static directory
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Create non-root user
RUN adduser --disabled-password --gecos '' app
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "ganoherb_inventory_billing.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1", "--max-requests", "1000", "--max-requests-jitter", "100", "--timeout", "120"]
