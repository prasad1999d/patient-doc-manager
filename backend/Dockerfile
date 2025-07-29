# backend/Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY . .

# Create uploads folder
RUN mkdir -p uploads

# Expose port and run app
EXPOSE 5000
CMD ["python", "app.py"]
