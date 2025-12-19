# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose Dash app port
EXPOSE 8050

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Default command: run main.py (agents)
CMD ["python3", "main.py"]

