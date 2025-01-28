# Use a slim Python image
FROM python:3.10-slim-bullseye

# Install Chrome & ChromeDriver
RUN apt-get update \
    && apt-get install -y chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Create and use a directory for your app
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entire codebase into /app
COPY . .

# EXPOSE the same port that Render will assign (commonly 10000)
EXPOSE 10000

# Gunicorn must bind to 0.0.0.0:$PORT, so we use the $PORT env variable
CMD ["gunicorn", "app:app", "--bind=0.0.0.0:$PORT"]
