FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY deployment/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code, model, and data
COPY deployment/src/ ./src/
COPY deployment/model.keras .
COPY deployment/data/ ./data/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=model.keras

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "src/app.py"]