FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create a non-root user and set up permissions
RUN useradd -m dev && \
    mkdir -p /app/data && \
    touch /app/conversation.jsonp && \
    chown -R dev:dev /app

USER dev

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "animalbot.py"]