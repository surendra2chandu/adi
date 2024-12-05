# Use an official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /src

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn

# Expose port 80
EXPOSE 89

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "89", "--reload"]