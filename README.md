# LogFileIntoCSV Lambda

This Lambda function fetches, processes, and uploads Nginx log files as CSV to either **GitHub** or **S3**. It includes features for filtering and sorting the log data.

## Functionality
- **Fetch**: The Lambda function fetches Nginx log files from a GitHub repository.
- **Filter**: The logs can be filtered by a specific field and value.
- **Sort**: The logs can be sorted by a specified field in ascending or descending order.
- **Upload**: The resulting CSV file can be uploaded to **GitHub** or **S3**.

## Usage

### API Endpoint

Use the following URL to call the Lambda function:

method: GET
url: https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com


### Query Parameters

- `log_file`: (optional) The name of the log file to fetch. Default: `nginx.log`.
- `upload`: (optional) The destination for uploading the processed file. Options:
  - `github`: Upload the CSV to GitHub.
  - `s3`: Upload the CSV to S3.
- `filter_field`: (optional) The field by which to filter the logs.
- `filtered_value`: (optional) The value for the filter.
- `order_field`: (optional) The field by which to sort the logs.
- `order_value`: (optional) The sort order. Options:
  - `asc`: Sort in ascending order.
  - `desc`: Sort in descending order.

### Example Requests
#### 1. Filter logs by `status` field and upload to S3
GET 
Here’s the updated README with the correct API Gateway URL included in all requests:

markdown
Copy
Edit
# LogFileIntoCSV Lambda

This Lambda function fetches, processes, and uploads Nginx log files as CSV to either **GitHub** or **S3**. It includes features for filtering and sorting the log data.

## Functionality
- **Fetch**: The Lambda function fetches Nginx log files from a GitHub repository.
- **Filter**: The logs can be filtered by a specific field and value.
- **Sort**: The logs can be sorted by a specified field in ascending or descending order.
- **Upload**: The resulting CSV file can be uploaded to **GitHub** or **S3**.

## Usage

### API Endpoint

Use the following URL to call the Lambda function:

https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com/GET

markdown
Copy
Edit

### Query Parameters

- `log_file`: (optional) The name of the log file to fetch. Default: `nginx.log`.
- `upload`: (optional) The destination for uploading the processed file. Options:
  - `github`: Upload the CSV to GitHub.
  - `s3`: Upload the CSV to S3.
- `filter_field`: (optional) The field by which to filter the logs.
- `filtered_value`: (optional) The value for the filter.
- `order_field`: (optional) The field by which to sort the logs.
- `order_value`: (optional) The sort order. Options:
  - `asc`: Sort in ascending order.
  - `desc`: Sort in descending order.

### Example Requests

#### 1. Filter logs by `status` field and upload to S3

**URL:**

https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com?log_file=nginx.log&upload=s3&filter_field=status&filtered_value=200

**Explanation:**
- `log_file=nginx.log`: Specifies the log file to fetch.
- `upload=s3`: Indicates that the result will be uploaded to **S3**.
- `filter_field=status`: Filters the logs by the `status` field.
- `filtered_value=200`: Includes only logs where the `status` field equals `200`.

#### 2. Sort logs by `datetime` in descending order and upload to GitHub

**URL:**
https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com?log_file=nginx.log&upload=github&order_field=datetime&order_value=desc


**Explanation:**
- `log_file=nginx.log`: Specifies the log file to fetch.
- `upload=github`: Indicates that the result will be uploaded to **GitHub**.
- `order_field=datetime`: Sorts the logs by the `datetime` field.
- `order_value=desc`: Sorts the logs in **descending** order based on the `datetime` field.

#### 3. Filter logs by `method` field, sort by `request_duration`, and upload to S3

**URL:**
https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com?log_file=nginx.log&upload=s3&filter_field=method&filtered_value=GET&order_field=request_duration&order_value=asc

**Explanation:**
- `log_file=nginx.log`: Specifies the log file to fetch.
- `upload=s3`: Indicates that the result will be uploaded to **S3**.
- `filter_field=method`: Filters the logs by the `method` field.
- `filtered_value=GET`: Includes only logs where the `method` field equals `GET`.
- `order_field=request_duration`: Sorts the logs by the `request_duration` field.
- `order_value=asc`: Sorts the logs in **ascending** order based on the `request_duration` field.

#### 4. No filter or sorting, upload to GitHub

**URL:**

https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com?log_file=nginx.log&upload=github


**Explanation:**
- `log_file=nginx.log`: Specifies the log file to fetch.
- `upload=github`: Indicates that the result will be uploaded to **GitHub**.
- No filtering or sorting applied (defaults to no filter and default sorting). 

### Environment Variables

Make sure the following environment variables are set for the Lambda function:
- `GITHUB_TOKEN`: The GitHub personal access token for authentication.
- `S3_BUCKET_NAME`: The name of the S3 bucket where the CSV file will be uploaded.

### Deployment

1. **Create Lambda Function**: Deploy the script to AWS Lambda.
2. **Set up API Gateway**: Configure API Gateway to trigger the Lambda function via HTTP requests.
3. **GitHub Repository**: Ensure the log files are available in the GitHub repository `AaronShemtov/LogFileIntoCSV`.
4. **Set up S3 Bucket**: Create the S3 bucket named `logs-result-csv` for uploading the processed logs.

### Notes
- The log files must be placed in the `logs_input/` folder of the GitHub repository.
- The resulting CSV file will be uploaded to the `logs-output/` folder in GitHub or the `logs-output/` folder in your S3 bucket.
