import re
import csv
import json
import requests
import boto3
import base64
from datetime import datetime
import os
import uuid


# Constants
GITHUB_REPO = "AaronShemtov/LogFileIntoCSV"  # GitHub Repository
RAW_GITHUB_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/logs_input/"
DEFAULT_LOG_FILE = "nginx.log"  # Default log file name

# S3 Configuration
S3_BUCKET_NAME = "logs-result-csv"
S3_OUTPUT_FOLDER = "logs-output/"

# Initialize S3 Client
s3 = boto3.client("s3")

# Get GitHub token from environment variables
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Dynamo DB
dynamodb = boto3.resource("dynamodb")
tabledb = dynamodb.Table("LambdaExecutionLogsLogFileIntoCSV")

# Regular expression pattern for parsing Nginx logs
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) - - \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>.*?) (?P<protocol>HTTP/\d\.\d)" (?P<status>\d+) (?P<response_size>\d+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)" (?P<request_duration>\d+) (?P<request_processing>\S+) \[(?P<service>[^\]]+)\] (?P<extra_info>\S+) (?P<upstream_ip>\S+) (?P<upstream_response_size>\d+) (?P<upstream_response_duration>\S+) (?P<final_response_code>\d+) (?P<request_id>\S+)'
)

def fetch_logs(log_file_name):
    """Fetch log file from GitHub repository."""
    log_file_url = f"{RAW_GITHUB_URL}{log_file_name}"
    print(f"Fetching log file from URL: {log_file_url}")

    try:
        response = requests.get(log_file_url)
        response.raise_for_status()
        print("Log file fetched successfully from GitHub.")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching log file: {str(e)}")
        raise FileNotFoundError(f"Log file {log_file_name} not found in GitHub repository.")

def parse_logs(log_data):
    """Parse logs using regex pattern."""
    print("Parsing log data using regex pattern.")
    parsed_data = []
    for line in log_data.splitlines():
        match = LOG_PATTERN.match(line)
        if match:
            parsed_data.append(match.groupdict())

    print(f"Parsed {len(parsed_data)} lines of log data.")
    return parsed_data

def filter_logs(parsed_data, filter_field, filter_value):
    """Filter parsed log data based on field and value."""
    print(f"Filtering logs by {filter_field} = {filter_value}.")
    return [entry for entry in parsed_data if entry.get(filter_field) == filter_value]

def sort_logs(parsed_data, order_field, order_value):
    """Sort parsed log data by field and order."""
    print(f"Sorting logs by {order_field} in {order_value} order.")
    return sorted(parsed_data, key=lambda x: x.get(order_field), reverse=(order_value == "desc"))

def upload_to_s3(parsed_data, log_file_name):
    """Uploads parsed log data to an S3 bucket."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_filename = f"output_{timestamp}.csv"
    s3_key = f"{S3_OUTPUT_FOLDER}{csv_filename}"

    # Convert parsed data to CSV format
    csv_content = "ip,datetime,method,request,protocol,status,response_size,referrer,user_agent,request_duration,request_processing,service,extra_info,upstream_ip,upstream_response_size,upstream_response_duration,final_response_code,request_id\n"
    for row in parsed_data:
        # Wrap fields with commas in double quotes (e.g., user_agent)
        csv_content += f"{row['ip']},{row['datetime']},{row['method']},{row['request']},{row['protocol']},{row['status']},{row['response_size']},{row['referrer']},\"{row['user_agent']}\",{row['request_duration']},{row['request_processing']},{row['service']},{row['extra_info']},{row['upstream_ip']},{row['upstream_response_size']},{row['upstream_response_duration']},{row['final_response_code']},{row['request_id']}\n"

    try:
        # Upload to S3
        s3.put_object(Body=csv_content, Bucket=S3_BUCKET_NAME, Key=s3_key)
        file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
        print(f"File uploaded successfully to S3: {file_url}")
        return {"message": "File uploaded successfully", "url": file_url}
    except Exception as e:
        print(f"Error uploading file to S3: {str(e)}")
        return {"error": f"Failed to upload file: {str(e)}"}

def upload_to_github(parsed_data, log_file_name):
    """Uploads parsed log data to GitHub repository."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_filename = f"output_{timestamp}.csv"
    file_path = f"logs_output/{csv_filename}"

    # Convert parsed data to CSV format
    csv_content = "ip,datetime,method,request,protocol,status,response_size,referrer,user_agent,request_duration,request_processing,service,extra_info,upstream_ip,upstream_response_size,upstream_response_duration,final_response_code,request_id\n"
    for row in parsed_data:
        # Wrap fields with commas in double quotes (e.g., user_agent)
        csv_content += f"{row['ip']},{row['datetime']},{row['method']},{row['request']},{row['protocol']},{row['status']},{row['response_size']},{row['referrer']},\"{row['user_agent']}\",{row['request_duration']},{row['request_processing']},{row['service']},{row['extra_info']},{row['upstream_ip']},{row['upstream_response_size']},{row['upstream_response_duration']},{row['final_response_code']},{row['request_id']}\n"

    github_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "message": f"Add log file {csv_filename}. File uploaded by Lambda",
        "content": base64.b64encode(csv_content.encode()).decode("utf-8"),
        "branch": "main"
    }

    try:
        response = requests.put(github_url, headers=headers, json=data)
        response.raise_for_status()
        print(f"File uploaded successfully to GitHub: {github_url}")
        return {"message": "File uploaded successfully", "url": github_url}
    except requests.exceptions.RequestException as e:
        print(f"Failed to upload file to GitHub: {str(e)}")
        return {"error": f"Failed to upload file: {str(e)}"}

def dynamodb_writing(log_file_name, upload_option, event_sender, filter, order):
    """Writing to DynamoDB."""

    # Generate unique execution ID
    execution_id = str(uuid.uuid4())
    
    # Store log in DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('LambdaExecutionLogsLogFileIntoCSV')
    
    table.put_item(
        Item={
            'ExecutionID': execution_id,
            'Record_Timestamp': datetime.utcnow().isoformat(),
            'FileName': log_file_name,
            'Upload_Option': upload_option,
            'Upload_Option': upload_option,
            'Event_sender' : event_sender,
            'Filter': filter,
            'Order': order
        }
    )




def lambda_handler(event, context):
    print("Lambda function started.")

    # Get path from the event
    path = event.get("rawPath", "/")

    if path == "/info":
        return get_execution_info()

    # Get log file name from query parameters (default to DEFAULT_LOG_FILE if not provided)
    log_file_name = event.get("queryStringParameters", {}).get("log_file", DEFAULT_LOG_FILE)
    upload_option = event.get("queryStringParameters", {}).get("upload", "github")
    filter_field = event.get("queryStringParameters", {}).get("filter_field", None)
    filter_value = event.get("queryStringParameters", {}).get("filter_value", None)
    order_field = event.get("queryStringParameters", {}).get("order_field", None)
    order_value = event.get("queryStringParameters", {}).get("order_value", None)
    event_sender = event.get("queryStringParameters", {}).get("event_sender", "user_api")

    try:
        log_data = fetch_logs(log_file_name)
        parsed_data = parse_logs(log_data)

        # Apply filtering if specified
        if filter_field and filter_value:
            filter = filter_field + "=" + filter_value
            parsed_data = filter_logs(parsed_data, filter_field, filter_value)
        else: filter = None

        # Apply sorting if specified
        if order_field and order_value:
            order = order_field + "=" + order_value
            parsed_data = sort_logs(parsed_data, order_field, order_value)
        else: order = None

        if upload_option == "s3":
            result = upload_to_s3(parsed_data, log_file_name)  # Uploading to S3
        else:
            result = upload_to_github(parsed_data, log_file_name)  # Default uploading to GitHub

        dynamodb_writing(log_file_name,upload_option,event_sender,filter,order)

        print("Lambda function completed successfully.")
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }
    except Exception as e:
        print(f"Lambda function error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }

def get_execution_info():
    """Retrieve stored execution logs from DynamoDB."""
    
    try:
        response = tabledb.scan()  # Get all logs
        logs = response.get("Items", [])
        
        return {
            "statusCode": 200,
            "body": json.dumps(logs, indent=2),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }