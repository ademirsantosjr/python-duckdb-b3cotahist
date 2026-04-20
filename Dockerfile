FROM python:3.14-slim

# System dependencies for high-performance math and compression
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8888 for Jupyter Lab (Analysis UI)
EXPOSE 8888

# Default command starts Jupyter in the /app folder
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]