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


### Query Parameters

- `log_file`: (optional) The name of the log file to fetch. Default: `nginx.log`.
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
https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com?log_file=nginx.log&upload=s3&filter_field=status&filter_value=200

- `log_file=nginx.log`: Specifies the log file to fetch.
- `upload=s3`: Indicates that the result will be uploaded to **S3**.
- `filter_field=status`: Filters the logs by the `status` field.
- `filter_value=200`: Includes only logs where the `status` field equals `200`.

#### 2. Sort logs by `datetime` in descending order and upload to GitHub

GET
https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com?log_file=nginx.log&upload=github&order_field=datetime&order_value=desc

- `log_file=nginx.log`: Specifies the log file to fetch.
- `upload=github`: Indicates that the result will be uploaded to **GitHub**.
- `order_field=datetime`: Sorts the logs by the `datetime` field.
- `order_value=desc`: Sorts the logs in **descending** order based on the `datetime` field.

#### 3. Filter logs by `method` field, sort by `request_duration`, and upload to S3

GET
https://32se2pmvb5.execute-api.eu-central-1.amazonaws.com?log_file=nginx.log&upload=s3&filter_field=method&filter_value=GET&order_field=request_duration&order_value=asc

- `log_file=nginx.log`: Specifies the log file to fetch.
- `upload=s3`: Indicates that the result will be uploaded to **S3**.
- `filter_field=method`: Filters the logs by the `method` field.
- `filter_value=GET`: Includes only logs where the `method` field equals `GET`.
- `order_field=request_duration`: Sorts the logs by the `request_duration` field.
- `order_value=asc`: Sorts the logs in **ascending** order based on the `request_duration` field.

# System design:
The entire workflow begins in the LogFileIntoCSV/lambda folder of the GitHub repository, where the core code for processing logs resides. Sensitive information, such as credentials and configuration settings, is securely stored in GitHub Secrets, ensuring that your environment variables remain private throughout the deployment process.

When changes are pushed to the main branch, the automated GitHub Actions flow is triggered. This initiates the creation of a Docker container, which packages your application along with all necessary dependencies. This container is then pushed to Amazon Elastic Container Registry (ECR), which acts as a secure storage repository for your container images.

Once the Docker image is uploaded to Amazon ECR, it becomes the foundation for deploying an AWS Lambda function. The Lambda function is launched directly from the ECR image, which means the container’s environment is replicated in AWS, ensuring consistency in execution. To facilitate interaction with the outside world, the Lambda function is exposed through an API Gateway, which is linked to the Lambda function using a simple GET request method.

When a request is made to this API Gateway endpoint, it triggers the Lambda function, which processes the Nginx log files. After processing, the resulting CSV file is uploaded to either Amazon S3 or GitHub, depending on the parameters specified in the request.

Additionally, to ensure secure and authorized interactions with GitHub, the GITHUB_TOKEN—which is essential for accessing the repository—is securely stored in Lambda environment variables, maintaining smooth integration with GitHub during the file upload process.
