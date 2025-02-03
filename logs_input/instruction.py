please rewrite python script so that field will be:

as in given example:
ip
datetime
method
request
protocol
status
response_size
referrer
user_agent 
request_duration
request_processing
service
extra_info
upstream_ip
upstream_response_size
upstream_response_duration
final_response_code
request_id

example:
{
    'ip': '192.168.226.64',
    'datetime': '26/Apr/2021:21:20:27 +0000',
    'method': 'GET',
    'request': '/api/datasources/proxy/1/api/v1/query_range?query=sum_over_time(probe_success%5B5s%5D)&start=1619471700&end=1619472000&step=30',
    'protocol': 'HTTP/2.0',
    'status': '200',
    'response_size': '87',
    'referrer': 'https://grafana.itoutposts.com/d/xtkCtBkiz/blackbox-exporter-overview?editview=settings&orgId=1&refresh=5s',
    'user_agent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36' 
    'request_duration': '118',
    'request_processing': '0.003',
    'service': 'monitoring-monitoring-prometheus-grafana-80',
    'extra_info': '',
     'upstream_ip': '192.168.226.102:3000',
'upstream_response_size':'201',
'upstream_response_duration':'0.012',
'final_response_code' : '200',
'request_id': '4503c9cfe2fac12a09cb27d871d26d0d',
}


please remake python script so that it will take file from local folder

C:\Users\Igor\LogFileIntoCSV\logs_input

file name nginx.log
generate CSV file

and save it in folder C:\Users\Igor\LogFileIntoCSV\logs_output



192.168.226.64 - - [26/Apr/2021:21:20:52 +0000] "GET /api/datasources/proxy/1/api/v1/query_range?query=probe_http_ssl%7Btarget%3D~%22()%22%7D&start=1619471730&end=1619472030&step=30 HTTP/2.0" 200 204 "https://grafana.itoutposts.com/d/xtkCtBkiz/blackbox-exporter-overview?editview=templating&orgId=1&refresh=5s" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36" 117 0.007 [monitoring-monitoring-prometheus-grafana-80] [] 192.168.226.102:3000 204 0.008 200 ee750efddfd03d0f547cdf7ab17298ac
192.168.226.64 - - [26/Apr/2021:21:20:52 +0000] "GET /api/datasources/proxy/1/api/v1/query_range?query=probe_http_status_code%7Btarget%3D~%22()%22%7D&start=1619471730&end=1619472030&step=30 HTTP/2.0" 200 210 "https://grafana.itoutposts.com/d/xtkCtBkiz/blackbox-exporter-overview?editview=templating&orgId=1&refresh=5s" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36" 123 0.008 [monitoring-monitoring-prometheus-grafana-80] [] 192.168.226.102:3000 210 0.008 200 f404e93ba6461513934930da3de65197
192.168.226.64 - - [26/Apr/2021:21:20:52 +0000] "GET /api/datasources/proxy/1/api/v1/query_range?query=probe_ssl_earliest_cert_expiry%7Btarget%3D~%22()%22%7D-time()&start=1619471730&end=1619472030&step=30 HTTP/2.0" 200 212 "https://grafana.itoutposts.com/d/xtkCtBkiz/blackbox-exporter-overview?editview=templating&orgId=1&refresh=5s" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36" 134 0.008 [monitoring-monitoring-prometheus-grafana-80] [] 192.168.226.102:3000 212 0.008 200 2005b9cef90826583d17e02ac57add2a
192.168.226.64 - - [26/Apr/2021:21:20:52 +0000] "GET /api/datasources/proxy/1/api/v1/query_range?query=avg(probe_duration_seconds%7Btarget%3D~%22()%22%7D)&start=1619471730&end=1619472030&step=30 HTTP/2.0" 200 226 "https://grafana.itoutposts.com/d/xtkCtBkiz/blackbox-exporter-overview?editview=templating&orgId=1&refresh=5s" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36" 128 0.004 [monitoring-monitoring-prometheus-grafana-80] [] 192.168.226.102:3000 226 0.004 200 98176824861eddfedb339a24b5c0b317
192.168.226.64 - - [26/Apr/2021:21:20:52 +0000] "GET /api/datasources/proxy/1/api/v1/query_range?query=avg(probe_dns_lookup_time_seconds%7Btarget%3D~%22()%22%7D)&start=1619471730&end=1619472030&step=30 HTTP/2.0" 200 206 "https://grafana.itoutposts.com/d/xtkCtBkiz/blackbox-exporter-overview?editview=templating&orgId=1&refresh=5s" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36" 133 0.004 [monitoring-monitoring-prometheus-grafana-80] [] 192.168.226.102:3000 206 0.004 200 5fcd7da71a550c2a56ca341e34faec55
192.168.226.64 - - [26/Apr/2021:21:20:52 +0000] "GET /api/datasources/proxy/1/api/v1/query_range?query=probe_duration_seconds%20and%20probe_success%20%3D%3D%201&start=1619471730&end=1619472030&step=30 HTTP/2.0" 200 290 "https://grafana.itoutposts.com/d/xtkCtBkiz/blackbox-exporter-overview?editview=templating&orgId=1&refresh=5s" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36" 128 0.003 [monitoring-monitoring-prometheus-grafana-80] [] 192.168.226.102:3000 290 0.004 200 ec2630b6d0fdd48e166142b2695a7357
192.168.226.64 - - [26/Apr/2021:21:20:52 +0000] "GET /api/datasources/proxy/1/api/v1/query_range?query=sum_over_time(probe_success%7Btarget%3D~%22()%22%7D%5B5s%5D)&start=1619471730&end=1619472030&step=30 HTTP/2.0" 200 87 "https://grafana.itoutposts.com/d/xtkCtBkiz/blackbox-exporter-overview?editview=templating&orgId=1&refresh=5s" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36" 134 0.005 [monitoring-monitoring-prometheus-grafana-80] [] 192.168.226.102:3000 87 0.008 200 d05dc93485d7c959c780382f4c3b4b6b
192.168.226.64 - - [26/Apr/2021:21:20:52 +0000] "GET /api/datasources/proxy/1/api/v1/query_range?query=sum_over_time(probe_success%5B5s%5D)&start=1619471730&end=1619472030&step=30 HTTP/2.0" 200 87 "https://grafana.itoutposts.com/d/xtkCtBkiz/blackbox-exporter-overview?editview=templating&orgId=1&refresh=5s" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36" 115 0.005 [monitoring-monitoring-prometheus-grafana-80] [] 192.168.226.102:3000 87 0.008 200 27650c30266ba1d7b57d5f99d33a94bf