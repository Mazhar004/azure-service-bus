# Use the official Python image from the Docker Hub
FROM python:3.11-slim as builder

# Set the working directory in the builder stage
WORKDIR /build

# Copy the requirements file into the builder
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir --user -r requirements.txt

# Start a new stage
FROM python:3.11-slim

# Install dumb-init and git
RUN set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    dumb-init \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the Python packages from the builder stage
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable:
ENV PATH=/root/.local:$PATH

# Copy the application files into the container
COPY client/ client/
COPY message/ message/
COPY utils/ utils/
COPY subscriber.py .
COPY .env .

RUN chmod +x subscriber.py

ENTRYPOINT ["dumb-init"]