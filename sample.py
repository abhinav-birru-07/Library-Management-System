import re
import argparse
from pprint import pprint
import logging
from collections import Counter, defaultdict


def parse_logs(log_lines):
    """
    Parses log lines and stores the details in a dictionary.

    Args:
    log_lines (list of str): List of log lines to be parsed.

    Returns:
    dict: Dictionary where the key is the IP address and the value is a list of request details in dictionary format.
    """
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>.*?)\] '
        r'"(?P<request_type>\w+) (?P<endpoint>.*?) HTTP/\d+\.\d+" '
        r'(?P<status_code>\d+) (?P<port>\d+)(?: "(?P<message>.*?)")?'
    )

    parsed_logs = {}

    for line in log_lines:
        # parse the log for match
        match = log_pattern.match(line)
        if match:
            log_data = match.groupdict()
            ip_address = log_data.pop('ip')

            # Store log data under the respective IP address
            if ip_address not in parsed_logs:
                parsed_logs[ip_address] = []
            # stores the log details under the ip address key
            parsed_logs[ip_address].append(log_data)

    return parsed_logs


def analyze_logs(parsed_logs):
    """Analyzes parsed logs to calculate required statistics."""
    requests_per_ip = Counter()
    accessed_endpoints = Counter()
    suspicious_activity = defaultdict(int)

    for log in parsed_logs:
        ip = log['ip']
        endpoint = log['endpoint']
        status_code = log['status_code']

        requests_per_ip[ip] += 1
        accessed_endpoints[endpoint] += 1

        if status_code == '401':  # Track failed login attempts
            suspicious_activity[ip] += 1

    return requests_per_ip, accessed_endpoints, suspicious_activity


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_file', '-lf', type=str, default='sample.log', required=False,
                        help="Log file name which has a log in each line")
    parser.add_argument('--output_file', '-of', type=str, default='log_analysis_results.csv', required=False,
                        help="Output file name(csv file) which is used to write the final results after analysis")

    args = parser.parse_args()
    log_file = args.log_file
    output_file = args.output_file
    try:
        with open(log_file, 'r') as fh:
            logging.info("Reading the log file {log_file}".format(log_file=log_file)) # using format for py2 compatibility
            log_lines = fh.readlines()
        logs_analysis = parse_logs(log_lines)
        logging.info("Logs analysis:")
        pprint(logs_analysis)

        with open()

    except FileNotFoundError as e:
        logging.error("File not found : {e}".format(e=e))
    except Exception as e:
        logging.error("Exception: {e}".format(e=e))



