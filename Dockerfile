FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all files to /app
COPY . .

# Make the launch script executable
RUN chmod +x /app/launch.sh

# Expose port
EXPOSE 7860

# Start container
CMD ["/app/launch.sh"]
