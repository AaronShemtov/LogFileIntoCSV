import re
import csv
from datetime import datetime

# Input and output file paths
input_file = r'C:\Users\Igor\LogFileIntoCSV\logs_input\nginx.log'
output_file = r'C:\Users\Igor\LogFileIntoCSV\logs_output\output.csv'

# Regular expression pattern to parse the log lines
log_pattern = re.compile(
    r'(?P<ip>\S+) - - \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>.*?) (?P<protocol>HTTP/\d\.\d)" (?P<status>\d+) (?P<response_size>\d+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)" (?P<request_duration>\d+) (?P<request_processing>\S+) \[(?P<service>[^\]]+)\] (?P<extra_info>\S+) (?P<upstream_ip>\S+) (?P<upstream_response_size>\d+) (?P<upstream_response_duration>\S+) (?P<final_response_code>\d+) (?P<request_id>\S+)'
)

# Function to parse each log line
def parse_log_line(line):
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    return None

# Open input log file and output CSV file
with open(input_file, 'r', encoding='utf-8') as log_file, open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=[
        'ip', 'datetime', 'method', 'request', 'protocol', 'status', 'response_size',
        'referrer', 'user_agent', 'request_duration', 'request_processing', 'service',
        'extra_info', 'upstream_ip', 'upstream_response_size', 'upstream_response_duration',
        'final_response_code', 'request_id'
    ])
    
    # Write header row in CSV
    csv_writer.writeheader()

    # Process each log line
    for line in log_file:
        log_data = parse_log_line(line)
        if log_data:
            # Format datetime to match the desired format
            log_data['datetime'] = datetime.strptime(log_data['datetime'], '%d/%b/%Y:%H:%M:%S +0000').strftime('%d/%b/%Y:%H:%M:%S +0000')
            # Write the log entry into CSV
            csv_writer.writerow(log_data)

print(f'CSV file has been created: {output_file}')
