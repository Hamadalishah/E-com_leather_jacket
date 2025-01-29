FROM python:3.12-slim  

# System dependencies install karo  
RUN apt-get update && apt-get install -y --no-install-recommends \  
    libpq-dev gcc \  
    && rm -rf /var/lib/apt/lists/*  

WORKDIR /app  

# Install Poetry  
RUN pip install poetry  

# Copy dependency files  
COPY pyproject.toml poetry.lock ./  

# Install Python dependencies  
RUN poetry config virtualenvs.create false \  
    && poetry install --only main --no-interaction --no-ansi  

# Copy application code  
COPY ./app ./app  

# Expose port  
EXPOSE 8004  

# Start command  
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"]  