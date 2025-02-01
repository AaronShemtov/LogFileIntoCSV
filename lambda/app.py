import re
import csv
import json
import logging
import requests
import boto3
from datetime import datetime

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Constants
GITHUB_REPO = "AaronShemtov/LogFileIntoCSV"  # GitHub Repository
RAW_GITHUB_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/input_logs/"
DEFAULT_LOG_FILE = "nginx.log"  # Default log file name

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
    """Fetch log file from GitHub repository."""
    log_file_url = f"{RAW_GITHUB_URL}{log_file_name}"
    logging.debug(f"Fetching log file from URL: {log_file_url}")
    
    try:
        response = requests.get(log_file_url)
        response.raise_for_status()
        logging.debug("Log file fetched successfully from GitHub.")
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching log file: {str(e)}")
        raise FileNotFoundError(f"Log file {log_file_name} not found in GitHub repository.")

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

def sort_logs(parsed_data, sort_by):
    """Sort parsed data based on the sort parameter."""
    try:
        sorted_data = sorted(parsed_data, key=lambda x: x.get(sort_by, ''), reverse=False)
        logging.debug(f"Logs sorted by {sort_by}")
        return sorted_data
    except KeyError:
        logging.error(f"Invalid sort key: {sort_by}")
        return parsed_data

def filter_logs(parsed_data, filter_key, filter_value):
    """Filter parsed data based on the filter parameter."""
    filtered_data = [entry for entry in parsed_data if entry.get(filter_key) == filter_value]
    logging.debug(f"Filtered logs by {filter_key} = {filter_value}. Filtered count: {len(filtered_data)}")
    return filtered_data

def upload_to_s3(parsed_data, log_file_name):
    """Uploads parsed log data to an S3 bucket."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_filename = f"output_{timestamp}.csv"
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
    
    # Get log file name from query parameters (default to DEFAULT_LOG_FILE if not provided)
    log_file_name = event.get("queryStringParameters", {}).get("log_file", DEFAULT_LOG_FILE)
    
    # Get sort parameter (default to None if not provided)
    sort_by = event.get("queryStringParameters", {}).get("sort", None)
    
    # Get filter parameter (default to None if not provided)
    filter_param = event.get("queryStringParameters", {}).get("filter", None)
    
    filter_key = None
    filter_value = None
    if filter_param:
        # Filter is in the form key=value, split it
        filter_key, filter_value = filter_param.split("=")
    
    try:
        log_data = fetch_logs(log_file_name)
        parsed_data = parse_logs(log_data)

        # Apply sorting if requested
        if sort_by:
            parsed_data = sort_logs(parsed_data, sort_by)

        # Apply filtering if requested
        if filter_key and filter_value:
            parsed_data = filter_logs(parsed_data, filter_key, filter_value)

        result = upload_to_s3(parsed_data, log_file_name)  # Upload to S3
        logging.info("Lambda function completed successfully.")
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }
    except Exception as e:
        logging.error(f"Lambda function error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
