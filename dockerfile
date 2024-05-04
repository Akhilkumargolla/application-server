# Use an appropriate base image (e.g., Alpine)
FROM docker.io/library/alpine:latest

# Install system dependencies
RUN apk update && \
    apk upgrade && \
    apk add --no-cache python3 py3-pip && \
    rm -rf /var/cache/apk/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Create a virtual environment
RUN python3 -m venv /venv

# Activate the virtual environment
ENV PATH="/venv/bin:$PATH"

# Install dependencies within the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

EXPOSE 5001

# Copy the application code
COPY . .

# Command to run the application
CMD ["python", "src/app.py"]
