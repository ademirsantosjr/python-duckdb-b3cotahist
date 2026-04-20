FROM python:3.14-slim

# Install dependencies for building Python packages (if needed)
RUN apt-get update && apt-get install -id --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# The container simply "exists", it will run commands via exec or docker-compose
CMD ["tail", "-f", "/dev/null"]