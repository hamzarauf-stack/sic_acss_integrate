# Use the official Python image from Docker Hub as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock ./

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Install the dependencies from Pipfile
RUN pipenv install --system --deploy

# Explicitly install uvicorn globally, if it wasn't included in Pipfile
RUN pip install uvicorn

# Explicitely install the psycopg2-binary for postgres
RUN pip install psycopg2-binary

# Copy the FastAPI app code into the container
COPY main.py .

# Specify the command to run the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ,"--reload"]
