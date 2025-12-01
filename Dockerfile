FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy pyproject.toml and poetry.lock first for caching
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-root

COPY manage.py /app/manage.py
COPY wait-for-it.sh /app/wait-for-it.sh
COPY entrypoint.sh /app/entrypoint.sh

COPY core/ /app/core/
COPY templates/ /app/templates/
COPY staticfiles/ /app/staticfiles/


COPY admin_portal/ /app/admin_portal/
COPY client/ /app/client/
COPY common/ /app/common/
COPY main/ /app/main/
COPY notification/ /app/notification/
COPY organization/ /app/organization/
COPY payment/ /app/payment/
COPY scheduling/ /app/scheduling/
COPY services/ /app/services/


# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Start app
ENTRYPOINT ["/app/entrypoint.sh"]
