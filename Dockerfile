FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


ENV POETRY_VIRTUALENVS_CREATE=false
RUN mkdir -p /app/logs

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN apt-get update && apt-get install -y python3-pip python3-venv build-essential libpq-dev curl \
    && python3 -m pip install --upgrade pip \
    && pip install poetry




# Copy pyproject.toml and poetry.lock first for caching
COPY pyproject.toml poetry.lock* /app/


# Add Poetry to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies
RUN poetry install --no-root


COPY . /app


# Make entrypoint executable and fix potential Windows line ending issues
RUN apt-get update && apt-get install -y dos2unix && \
    dos2unix /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh


# Start app
ENTRYPOINT ["/app/entrypoint.sh"]
