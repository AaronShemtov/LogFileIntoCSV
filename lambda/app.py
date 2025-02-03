import csv
import re

def parse_log_line(line):
    # Regular expression to capture the relevant parts of each log line
    log_pattern = r'(?P<ip>[\d\.]+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<url>\S+) HTTP/[\d\.]+" (?P<status_code>\d+) (?P<response_size>\d+) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)" (?P<request_time>\d+) (?P<upstream_response_time>\d+\.\d+) \[(?P<upstream_name>[^\]]+)\] \[\] (?P<server_ip>[\d\.]+):(?P<server_port>\d+) (?P<response_size_2>\d+) (?P<request_time_2>\d+\.\d+) (?P<status_code_2>\d+) (?P<request_id>\w+)'
    
    match = re.match(log_pattern, line)
    
    if match:
        log_data = match.groupdict()

        # Parse user_agent to separate components
        user_agent = log_data['user_agent']
        ua_pattern = r'(?P<browser>[\w]+(?:/[\d\.]+)?) \((?P<os>[^)]+)\) (?P<webkit_version>AppleWebKit/[0-9\.]+) \((?P<engine>KHTML, like Gecko)\) (?P<chrome_version>Chrome/[0-9\.]+) (?P<safari_version>Safari/[0-9\.]+)'
        ua_match = re.match(ua_pattern, user_agent)

        if ua_match:
            ua_data = ua_match.groupdict()
            log_data.update(ua_data)
        
        return log_data
    else:
        return None

def parse_log_file(file_path, output_csv_path):
    with open(file_path, 'r') as log_file, open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = [
            'ip', 'timestamp', 'method', 'url', 'status_code', 'response_size', 'referer', 
            'user_agent', 'request_time', 'upstream_response_time', 'upstream_name', 'server_ip',
            'server_port', 'response_size_2', 'request_time_2', 'status_code_2', 'request_id',
            'browser', 'os', 'webkit_version', 'engine', 'chrome_version', 'safari_version'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for line in log_file:
            parsed_data = parse_log_line(line)
            if parsed_data:
                writer.writerow(parsed_data)

if __name__ == "__main__":
    log_file_path = 'access.log'  # Replace with your log file path
    output_csv_file = 'parsed_logs.csv'  # Output CSV file path
    parse_log_file(log_file_path, output_csv_file)
