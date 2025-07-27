FROM python:3.13-slim

# Set workdir
WORKDIR /app

FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install build tools needed for packages like argon2, psycopg2-binary, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libpq-dev \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . /app

# Set env vars
ENV PYTHONUNBUFFERED=1

# Expose API port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
