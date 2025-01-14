FROM python:3.12

LABEL maintainer="Syed Hamad Ali"

# Set the working directory in the container
WORKDIR /code

# Install Poetry
RUN pip install poetry

COPY . /code/


RUN poetry config virtualenvs.create false

RUN poetry install

# Copy the rest of the application code

# Expose port 8004
EXPOSE 8004

# Define the default command
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload", "--log-level", "debug"]
