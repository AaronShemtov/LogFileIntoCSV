# LogFileIntoCSV

There are 2 levels of program.
The first one which is mentioned in task.

And the second one is:





The filter options available are based on the fields defined in the log format. Here's a breakdown of the fields you can filter by, based on the log structure:

Available Filter Fields:
ip: The IP address of the client making the request.
datetime: The timestamp when the request was made (e.g., 26/Apr/2021:21:20:17 +0000).
method: The HTTP method used in the request (e.g., GET, POST).
request: The request path or URL (e.g., /api/annotations).
protocol: The HTTP protocol used in the request (e.g., HTTP/2.0).
status: The HTTP status code returned by the server (e.g., 200, 404).
response_size: The size of the response in bytes.
referrer: The referring URL, if available.
user_agent: The user agent string representing the client (browser/device) making the request.
request_duration: The total duration of the request in seconds.
request_processing: Time taken to process the request (usually a sub-segment of the total request duration).
service: The name of the service handling the request (e.g., monitoring-prometheus-grafana).
extra_info: Any additional info logged with the request (can be empty in some cases).
upstream_ip: The IP address of the upstream service handling the request.
upstream_response_size: The size of the response from the upstream service in bytes.
upstream_response_duration: The duration of the upstream response.
final_response_code: The final HTTP status code after processing the request.
request_id: A unique identifier for the request, used for tracing.
Example Filter Queries:
Filter by IP address: /GET?filter=ip,162.55.33.98
Filter by status code: /GET?filter=status,200
Filter by method: /GET?filter=method,GET
Filter by user agent: /GET?filter=user_agent,Mozilla/5.0