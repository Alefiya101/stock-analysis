FROM python:3.9

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file into the container
COPY ./backend/requirements.txt /code/

# Install the requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the backend code
COPY ./backend /code/

# Hugging Face Spaces runs on port 7860 by default
# We use uvicorn to serve the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
