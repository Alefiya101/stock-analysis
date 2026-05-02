# Stage 1: Build the React frontend
FROM node:18 AS frontend-builder
WORKDIR /app/frontend
# Copy package files and install dependencies
COPY frontend/package*.json ./
RUN npm install
# Copy the rest of the frontend code and build
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the FastAPI backend and serve the monolith
FROM python:3.9-slim

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file into the container
COPY ./backend/requirements.txt /code/

# Install the requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the backend code
COPY ./backend /code/

# Copy the built frontend from Stage 1 into the container
# main.py expects it at ../frontend/dist relative to the backend directory
COPY --from=frontend-builder /app/frontend/dist /frontend/dist

# Railway assigns a dynamic PORT environment variable.
# Using the shell form of CMD allows environment variable expansion.
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
