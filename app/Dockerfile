FROM python:3.12-slim  

# System dependencies  
RUN apt-get update && apt-get install -y --no-install-recommends \  
    libpq-dev gcc python3-dev musl-dev \  
    && rm -rf /var/lib/apt/lists/*  

WORKDIR /app  

# Install Poetry with specific version  
RUN pip install "poetry==1.8.2"  

# Copy dependencies  
COPY pyproject.toml poetry.lock ./  

# Install Python deps  
RUN poetry config virtualenvs.create false \  
    && poetry install --only main --no-interaction --no-ansi  

# Copy app code  
COPY ./app ./app  

EXPOSE 8004  
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"]  