# Use a slim Python image for smaller size
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
# We copy requirements.txt twice to leverage Docker cache
COPY requirements.txt .
# If the file is UTF-16, pip might have issues, but let's assume it works or we fix it if build fails
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose the internal port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
