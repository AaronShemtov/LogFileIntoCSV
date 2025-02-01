import re
import csv
import requests
import os
import json
import logging
from datetime import datetime
from github import Github

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Constants in app
REPO_NAME = "AaronShemtov/LogFileIntoCSV"  # Repository name
LOG_FILE_NAME = "nginx.log"  # Log file name in the repo
CSV_OUTPUT_PREFIX = "output"  # Prefix for the output file

# GitHub Raw Log URL
LOG_FILE_URL = f"https://raw.githubusercontent.com/{REPO_NAME}/main/{LOG_FILE_NAME}"

# Regex pattern for parsing Nginx logs
LOG_PATTERN = re.compile(
    r'(?P<ip>[\d\.]+) - - \[(?P<date>.*?)\] "(?P<method>\w+) (?P<url>.*?) (?P<protocol>HTTP/\d\.\d)" (?P<status>\d+) (?P<size>\d+)'
)

def fetch_logs():
    """Fetch log file from GitHub repository."""
    logging.debug(f"Fetching log file from URL: {LOG_FILE_URL}")
    
    try:
        response = requests.get(LOG_FILE_URL)
        response.raise_for_status()
        logging.debug("Log file fetched successfully.")
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching log file: {str(e)}")
        raise

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

def push_to_github(parsed_data):
    """Push parsed log data to GitHub as a new file."""
    GITHUB_TOKEN = os.getenv("G_TOKEN")

    if GITHUB_TOKEN is None:
        logging.error("Error: 'G_TOKEN' environment variable is not set!")
        raise ValueError("GitHub token not found.")
    
    logging.debug("GitHub Token retrieved successfully.")
    
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        logging.debug(f"Repository '{REPO_NAME}' found on GitHub.")

        # Convert parsed data to CSV format (in-memory)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_filename = f"{CSV_OUTPUT_PREFIX}_{timestamp}.csv"
        
        csv_content = "ip,date,method,url,protocol,status,size\n"
        for row in parsed_data:
            csv_content += f"{row['ip']},{row['date']},{row['method']},{row['url']},{row['protocol']},{row['status']},{row['size']}\n"

        # Upload to GitHub
        logging.debug(f"Uploading parsed log data to GitHub as {csv_filename}.")
        repo.create_file(f"logs/{csv_filename}", "Add parsed logs", csv_content)
        logging.info(f"File {csv_filename} successfully uploaded to GitHub.")
        return {"message": f"File {csv_filename} successfully uploaded to GitHub."}

    except Exception as e:
        logging.error(f"Error uploading file to GitHub: {str(e)}")
        return {"error": f"Failed to upload {csv_filename}: {str(e)}"}

def lambda_handler(event, context):
    """AWS Lambda handler function."""
    logging.info("Lambda function started.")
    
    try:
        log_data = fetch_logs()
        parsed_data = parse_logs(log_data)
        result = push_to_github(parsed_data)
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
