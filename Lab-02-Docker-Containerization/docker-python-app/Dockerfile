# Use official lightweight Python base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Leverage layer caching by copying dependencies first
COPY requirements.txt .

# Install dependencies without caching pip wheels to reduce image footprint
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app.py .

# Expose application port
EXPOSE 5000

# Specify execution command
CMD ["python", "app.py"]
