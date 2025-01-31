import re
import csv
import requests
import os
import json
from datetime import datetime
from github import Github
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants in app
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub Token
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
    response = requests.get(LOG_FILE_URL)
    response.raise_for_status()
    return response.text

def parse_logs(log_data):
    """Parse logs using regex pattern."""
    parsed_data = []
    for line in log_data.splitlines():
        match = LOG_PATTERN.match(line)
        if match:
            parsed_data.append(match.groupdict())
    return parsed_data

def push_to_github(parsed_data):
    """Push parsed log data to GitHub as a new file."""
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Convert parsed data to CSV format (in-memory)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_filename = f"{CSV_OUTPUT_PREFIX}_{timestamp}.csv"
    
    csv_content = "ip,date,method,url,protocol,status,size\n"
    for row in parsed_data:
        csv_content += f"{row['ip']},{row['date']},{row['method']},{row['url']},{row['protocol']},{row['status']},{row['size']}\n"

    # Upload to GitHub
    try:
        repo.create_file(f"logs/{csv_filename}", "Add parsed logs", csv_content)
        return {"message": f"File {csv_filename} successfully uploaded to GitHub."}
    except Exception as e:
        return {"error": f"Failed to upload {csv_filename}: {str(e)}"}

def lambda_handler(event, context):
    """AWS Lambda handler function."""
    try:
        log_data = fetch_logs()
        parsed_data = parse_logs(log_data)
        result = push_to_github(parsed_data)
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

