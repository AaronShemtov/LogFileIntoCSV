# Use a Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script and requirements file into the container
COPY . /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for GitHub token (optional, recommended to use a .env file)
# ENV GITHUB_TOKEN=<your_token_here>

# Run the Python script when the container starts
CMD ["python", "LogToCSV.py"]