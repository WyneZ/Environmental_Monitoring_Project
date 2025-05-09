# # Use official Python image
# FROM python:3.11-slim
# 
# # Set work directory
# WORKDIR /app
# 
# # Copy project files
# COPY . .
# 
# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt
# 
# # Run FastAPI with uvicorn
# CMD ["uvicorn", "combination:app", "--host", "0.0.0.0", "--port", "8000"]





# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "combination:app", "--host", "0.0.0.0", "--port", "8000"]
