FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_PATH=/app/model.pkl \
    PORT=5000

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Train model (in a real project, model might be stored elsewhere)
RUN python src/model/train.py

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.api.app:app"]