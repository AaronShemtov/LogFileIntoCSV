# Use AWS Lambda's Python base image
FROM public.ecr.aws/lambda/python:3.9

# Set the working directory
WORKDIR /var/task

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY app.py .


# Set the Lambda function handler
CMD ["app.lambda_handler"]
