import re
import csv
import os
import json
import logging
from datetime import datetime
import boto3

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Constants
DEFAULT_LOG_FILE = "nginx.log"  # Default log file name
INPUT_LOGS_FOLDER = "input_logs/"  # Folder where logs are stored in GitHub root directory
CSV_OUTPUT_PREFIX = "output"  # Prefix for the output file

# S3 Configuration
S3_BUCKET_NAME = "logs-result-csv"
S3_OUTPUT_FOLDER = "logs-output/"

# Initialize S3 Client
s3 = boto3.client("s3")

# Regex pattern for parsing Nginx logs
LOG_PATTERN = re.compile(
    r'(?P<ip>[\d\.]+) - - \[(?P<date>.*?)\] "(?P<method>\w+) (?P<url>.*?) (?P<protocol>HTTP/\d\.\d)" (?P<status>\d+) (?P<size>\d+)'
)

def fetch_logs(log_file_name):
    """Fetch log file from local storage."""
    log_file_path = os.path.join(INPUT_LOGS_FOLDER, log_file_name)
    logging.debug(f"Fetching log file from path: {log_file_path}")
    
    if not os.path.exists(log_file_path):
        logging.error(f"Log file {log_file_name} not found.")
        raise FileNotFoundError(f"Log file {log_file_name} not found.")
    
    with open(log_file_path, "r") as file:
        log_data = file.read()
    
    logging.debug("Log file read successfully.")
    return log_data

def parse_logs(log_data):
    """Parse logs using regex pattern."""
    logging.debug("Parsing log data using regex pattern.")
    parsed_data = []
    for line in log_data.splitlines():
        match = LOG_PATTERN.match(line)
        if match:
            parsed_data.append(match.groupdict())
    logging.debug(f"Parsed {len(parsed_data)} lines of log data.")
    return parsed_data

def upload_to_s3(parsed_data):
    """Uploads parsed log data to an S3 bucket."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_filename = f"{CSV_OUTPUT_PREFIX}_{timestamp}.csv"
    s3_key = f"{S3_OUTPUT_FOLDER}{csv_filename}"  # Full S3 path

    # Convert parsed data to CSV format
    csv_content = "ip,date,method,url,protocol,status,size\n"
    for row in parsed_data:
        csv_content += f"{row['ip']},{row['date']},{row['method']},{row['url']},{row['protocol']},{row['status']},{row['size']}\n"

    try:
        # Upload to S3
        s3.put_object(Bucket=S3_BUCKET_NAME, Key=s3_key, Body=csv_content, ContentType="text/csv")
        
        # Generate Public URL
        file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

        logging.info(f"File uploaded successfully to S3: {file_url}")
        return {"message": "File uploaded successfully", "url": file_url}

    except Exception as e:
        logging.error(f"Error uploading file to S3: {str(e)}")
        return {"error": f"Failed to upload file: {str(e)}"}

def lambda_handler(event, context):
    """AWS Lambda handler function."""
    logging.info("Lambda function started.")
    
    # Get log file name from event, default to DEFAULT_LOG_FILE
    log_file_name = event.get("log_file", DEFAULT_LOG_FILE)
    
    try:
        log_data = fetch_logs(log_file_name)
        parsed_data = parse_logs(log_data)
        result = upload_to_s3(parsed_data)  # Upload to S3
        logging.info("Lambda function completed successfully.")
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }
    except Exception as e:
        logging.error(f"Lambda function error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
