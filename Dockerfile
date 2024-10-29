# Use a multi-stage build to optimize the image size
FROM python:3.12-slim as base

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt ./  # Assuming the file is in the root directory

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Stage 1: Copy Flask API files
FROM base as flask_api

# Copy the Flask API files
COPY flask_api/ ./flask_api/

# Stage 2: Copy Streamlit app files
FROM base as streamlit_app

# Copy the Streamlit app files
COPY streamlit_app/ ./streamlit_app/

# Expose the ports for Flask API and Streamlit app
EXPOSE 5000 8501

# Start both applications
CMD ["sh", "-c", "python flask_api/app.py & streamlit run streamlit_app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]
