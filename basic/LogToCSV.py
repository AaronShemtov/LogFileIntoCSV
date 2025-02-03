import re
import csv
import requests
import os
from datetime import datetime
from github import Github
from dotenv import load_dotenv  # Import the load_dotenv function

# Load environment variables from .env file
load_dotenv()  # This loads variables from the .env file

# Constants
GITHUB_TOKEN = os.getenv("token")  # GitHub Token
REPO_NAME = "AaronShemtov/LogFileIntoCSV"  # Repository name
LOG_FILE_NAME = "nginx.log"  # Log file name in the repo
CSV_OUTPUT_PREFIX = "output"  # Prefix for the output file

# URL to fetch log file from GitHub
LOG_FILE_URL = f"https://raw.githubusercontent.com/{REPO_NAME}/main/{LOG_FILE_NAME}"

# Regex pattern for parsing Nginx logs
LOG_PATTERN = re.compile(r'(?P<ip>[\d\.]+) - - \[(?P<date>.*?)\] "(?P<method>\w+) (?P<url>.*?) (?P<protocol>HTTP/\d\.\d)" (?P<status>\d+) (?P<size>\d+)')

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

def save_to_csv(parsed_data, filename):
    """Save parsed log data to CSV file."""
    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["ip", "date", "method", "url", "protocol", "status", "size"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(parsed_data)

def push_to_github(filename):
    """Push the CSV file to the GitHub repository."""
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    with open(filename, "r") as file:
        content = file.read()
    try:
        repo.create_file(f"logs/{filename}", "Add parsed logs", content)
        print(f"File {filename} successfully uploaded.")
    except Exception as e:
        print(f"Failed to upload {filename}: {e}")

def main():
    """Main execution function."""
    log_data = fetch_logs()
    parsed_data = parse_logs(log_data)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"{CSV_OUTPUT_PREFIX}_{timestamp}.csv"
    save_to_csv(parsed_data, output_filename)
    push_to_github(output_filename)
    print("Logs processed and uploaded successfully.")

if __name__ == "__main__":
    main()
