FROM python:3.10-slim-bullseye

# 1) Install Chrome & ChromeDriver from apt
RUN apt-get update \
    && apt-get install -y chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# 2) Copy your code and install Python deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["gunicorn", "app:app"]
