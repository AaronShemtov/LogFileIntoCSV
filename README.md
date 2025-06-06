# System design

The workflow starts in the LogFileIntoCSV/lambda folder, where the core log processing code resides. Sensitive credentials and configurations are securely stored in GitHub Secrets.

When changes are pushed to the main branch, GitHub Actions triggers a workflow that builds a Docker container with the application and dependencies. This container is pushed to Amazon ECR and used to deploy an AWS Lambda function. The Lambda function is exposed via an Amazon API Gateway with a GET request endpoint https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com.

When triggered, the Amazon Lambda function processes Nginx log files and uploads the resulting CSV to either Amazon S3 or GitHub, based on request parameters. The GITHUB_TOKEN for repository access is securely stored in Lambda environment variables.

<img src="/structure.svg" alt="Project Screenshot" width="500"/>

Each run of lambda function is stored in DynamoDB.
In addition each 12 hours crone EventBridge Scheduler is ran that triggers Lambda Function.

All runs of Lambda function can be checked by request:
GET https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com/info

# LogFileIntoCSV Lambda

This Lambda function fetches, processes, and uploads Nginx log files as CSV to either **GitHub** or **S3**. It includes features for filtering and sorting the log data.

## Functionality
- **Fetch**: The Lambda function fetches Nginx log files (`nginx.log` file by default) from a GitHub repository .
- **Filter**: The logs can be filtered by a specific field and value.
- **Sort**: The logs can be sorted by a specified field in ascending or descending order.
- **Upload**: The resulting CSV file can be uploaded to **GitHub** (by default) or **S3**.

## Usage

### API Endpoint

The following request to call the Lambda function should be used:

method: GET
url: https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com

By default the 'nginx.log' log file is taken, converting it to CSV file and uploading it to 'LogFileIntoCSV/logs_output/' git repository with name 'output_[timestamp].csv'

Response of request has the form:

{"message": "File uploaded successfully", "url": "https://api.github.com/repos/AaronShemtov/LogFileIntoCSV/contents/logs_output/output_2025-02-03_17-46-50.csv"}

### Query Parameters

- `log_file`: (optional) The name of the log file to fetch. Default: `nginx.log`.
 If the log file is not found in repository the response will be presented:
 {"error": "Log file {file_name} not found in GitHub repository."}
- `upload`: (optional) The destination for uploading the processed file. Options:
  - `github`: Upload the CSV to GitHub.
  - `s3`: Upload the CSV to S3.
- `filter_field`: (optional) The field by which to filter the logs.
- `filter_value`: (optional) The value for the filter.
- `order_field`: (optional) The field by which to sort the logs.
- `order_value`: (optional) The sort order. Options:
  - `asc`: Sort in ascending order.
  - `desc`: Sort in descending order.

### Example Requests

#### 1. Filter logs by `status` field and upload to S3

GET
https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com?log_file=nginx_second_file.log&upload=s3&filter_field=status&filter_value=200

- `log_file=nginx_second_file.log`: Specifies the log file to fetch.
- `upload=s3`: Indicates that the result will be uploaded to **S3**.
- `filter_field=status`: Filters the logs by the `status` field.
- `filter_value=200`: Includes only logs where the `status` field equals `200`.

Example of response: {"message": "File uploaded successfully", "url": "https://logs-result-csv.s3.amazonaws.com/logs-output/output_2025-02-03_18-18-42.csv"}

Resulting file can be downloaded by pressink on the link:
https://logs-result-csv.s3.amazonaws.com/logs-output/output_2025-02-03_18-18-42.csv

#### 2. Sort logs by `datetime` in descending order and upload to GitHub

GET
https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com?log_file=nginx.log&upload=github&order_field=datetime&order_value=desc

- `log_file=nginx.log`: Specifies the log file to fetch.
- `upload=github`: Indicates that the result will be uploaded to **GitHub**.
- `order_field=datetime`: Sorts the logs by the `datetime` field.
- `order_value=desc`: Sorts the logs in **descending** order based on the `datetime` field.

Example of response: {"message": "File uploaded successfully", "url": "https://api.github.com/repos/AaronShemtov/LogFileIntoCSV/contents/logs_output/output_2025-02-03_18-16-03.csv"}

Resulting file can be downloaded by the name from github:
'LogFileIntoCSV/logs_output/output_2025-02-03_18-16-03.csv'


#### 3. Filter logs by `method` field, sort by `request_duration`, and upload to S3

GET
https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com?log_file=nginx.log&upload=s3&filter_field=method&filter_value=GET&order_field=request_duration&order_value=asc

- `log_file=nginx.log`: Specifies the log file to fetch.
- `upload=s3`: Indicates that the result will be uploaded to **S3**.
- `filter_field=method`: Filters the logs by the `method` field.
- `filter_value=GET`: Includes only logs where the `method` field equals `GET`.
- `order_field=request_duration`: Sorts the logs by the `request_duration` field.
- `order_value=asc`: Sorts the logs in **ascending** order based on the `request_duration` field.

Example of response: {"message": "File uploaded successfully", "url": "https://logs-result-csv.s3.amazonaws.com/logs-output/output_2025-02-03_18-11-15.csv"}

Resulting file can be downloaded by pressink on the link:
https://logs-result-csv.s3.amazonaws.com/logs-output/output_2025-02-03_18-11-15.csv

#### 4. Filter logs by `upstream_response_duration` field, sort by `upstream_response_size`, and upload to S3

GET
https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com?upload=s3&filter_field=upstream_response_duration&filter_value=0.004&order_field=upstream_response_size&order_value=desc

- `log_file=nginx.log`: this file will be processed by default.
- `upload=s3`: Indicates that the result will be uploaded to **S3**.
- `filter_field=upstream_response_duration`: Filters the logs by the `upstream_response_duration` field.
- `filter_value=0.004`: Includes only logs where the `upstream_response_duration` field equals `0.004`.
- `order_field=upstream_response_size`: Sorts the logs by the `upstream_response_size` field.
- `order_value=desc`: Sorts the logs in **descending** order based on the `upstream_response_size` field.

Example of response: {"message": "File uploaded successfully", "url": "https://logs-result-csv.s3.amazonaws.com/logs-output/output_2025-02-03_18-02-40.csv"}

Resulting file can be downloaded by pressink on the link:
https://logs-result-csv.s3.amazonaws.com/logs-output/output_2025-02-03_18-02-40.csv


# Possible Improvments

For the moment not all of fields are supported. In order to do that requests with body should be implementes and app.py script should be enhanced accordingly so that it will be able to work with it.

As well, as sorting and filtering with more than 1 fields together can be presented. For the moment API works only with 1 order field and 1 sorting field.

There fiels currently are not supported for using with filter parameter: **datetime**, **request**, **referrer**, **user_agent**. 
