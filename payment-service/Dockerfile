FROM python:3.10-slim

# Set working directory
WORKDIR /payment-service

# Install dependencies
COPY venv.txt .
RUN pip install --no-cache-dir -r venv.txt

# Copy the application
COPY . .

# Expose the app port
EXPOSE 3001

# Run the app
CMD ["python", "main.py"]
