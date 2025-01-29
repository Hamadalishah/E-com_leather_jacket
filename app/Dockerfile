# Stage 1: Builder (Install dependencies)  
FROM python:3.12-slim as builder  

WORKDIR /app  

# Install system deps + poetry  
RUN apt-get update && apt-get install -y --no-install-recommends curl \  
    && pip install "poetry==1.8.2" \  
    && rm -rf /var/lib/apt/lists/*  

# Copy only dependency files first  
COPY pyproject.toml poetry.lock ./  

# Install deps without virtualenv (production-only)  
RUN poetry config virtualenvs.create false \  
    && poetry install --only main --no-interaction --no-ansi  

# Stage 2: Runtime (Minimal image)  
FROM python:3.12-slim  

WORKDIR /app  

# Copy installed deps from builder  
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages  
COPY --from=builder /usr/local/bin /usr/local/bin  

# Copy application code  
COPY ./app ./app  


# Production configs  
ENV PYTHONUNBUFFERED=1 \  
    PYTHONPATH=/app \  
    APP_ENV=production  

EXPOSE 8004  

# Health check (Render compatible)  
HEALTHCHECK --interval=30s --timeout=5s \  
  CMD curl --fail http://localhost:8004/health || exit 1  

# Start command  
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"]  