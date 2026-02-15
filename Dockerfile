FROM python:3.9-slim

WORKDIR /app

# Install build dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY main.py .

# Command to run the script
CMD ["python", "main.py"]