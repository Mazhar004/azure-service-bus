# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# PYTHONUNBUFFERED ensures that Python output is sent straight to terminal (i.e. your container log) without being first buffered and that you can see the output of your application (e.g., Django logs) in real time.
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set an environment variable to specify the path to the .env file
ENV ENV_FILE_PATH=/app/.env

# Ensure entrypoint.sh is executable
RUN chmod +x /app/entrypoint.sh

# Default command to run when starting the container
ENTRYPOINT ["./entrypoint.sh"]