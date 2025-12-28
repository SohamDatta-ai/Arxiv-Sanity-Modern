# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GEMINI_API_KEY="AIzaSyAOpc7SYwr0yf1VfmD8LjI8CqwK3qCiFiw"

# Install system dependencies (build-essential for some python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Initialization script to fetch papers if DB is empty, then start server
CMD ["sh", "-c", "python scripts/fetch_papers.py && python -m app.main"]
