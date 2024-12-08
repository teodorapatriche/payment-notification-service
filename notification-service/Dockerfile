FROM python:3.10-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    gcc

# Set working directory
WORKDIR /notification-service

# Copy the requirements file
COPY venv.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r venv.txt

# Copy the application code
COPY . .

# Expose the service port
EXPOSE 3002

# Run the application
CMD ["python", "notify.py"]
