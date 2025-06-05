FROM python:3.10-slim

WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary log directories with proper permissions
RUN mkdir -p /opt/app/logs /app/logs /app/prediction_logs
RUN chmod -R 777 /opt/app/logs /app/logs /app/prediction_logs

# Expose application port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Define volumes for logs
VOLUME ["/app/logs", "/app/prediction_logs", "/opt/app/logs"]

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]