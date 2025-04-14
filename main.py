import re
import pandas as pd
import logging

# Configure logger
logging.basicConfig(
    filename='log_analysis.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


def parse_log_line(log_line):
    """
    Parses a single log line and extracts key details.
    """
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>.*?)\] '
        r'"(?P<request_type>\w+) (?P<endpoint>.*?) HTTP/\d+\.\d+" '
        r'(?P<status_code>\d+) (?P<port>\d+)(?: "(?P<message>.*?)")?'
    )
    match = log_pattern.match(log_line)
    if match:
        return match.groupdict()
    else:
        logger.warning(f"Failed to parse log line: {log_line}")
        return None


def read_and_parse_log_file(file_path):
    """
    Reads a log file and parses each line into a DataFrame.
    """
    parsed_logs = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                log_data = parse_log_line(line)
                if log_data:
                    parsed_logs.append(log_data)
        logger.info(f"Successfully parsed {len(parsed_logs)} log entries from {file_path}.")
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
    return pd.DataFrame(parsed_logs)


def analyze_requests_per_ip(df):
    """
    Analyzes the number of requests per IP.
    """
    requests_per_ip = df['ip'].value_counts().reset_index()
    requests_per_ip.columns = ['IP Address', 'Request Count']
    logger.info("Analyzed Requests per IP.")
    return requests_per_ip


def analyze_most_accessed_endpoint(df):
    """
    Analyzes the most accessed endpoint.
    """
    endpoint_counts = df['endpoint'].value_counts().reset_index().head(1)
    endpoint_counts.columns = ['Endpoint', 'Access Count']
    logger.info("Analyzed Most Accessed Endpoint.")
    return endpoint_counts


def analyze_suspicious_activity(df):
    """
    Analyzes suspicious activity (failed logins) for each IP.
    """
    failed_logins = df[(df['status_code'] == '401') | (df['message'].str.contains('invalid credentials', case=False, na=False))]
    failed_attempts_per_ip = failed_logins['ip'].value_counts().reset_index()
    failed_attempts_per_ip.columns = ['IP Address', 'Failed Login Count']
    logger.info("Analyzed Suspicious Activity for failed logins.")
    return failed_attempts_per_ip


def display_results(title, df):
    """
    Displays a DataFrame with a title in a clear, organized format.
    """
    logger.info(f"\n{'=' * 50}\n{title}\n{'=' * 50}")
    logger.info(f"\n{df.head(10).to_string(index=False)}\n")


def main():
    log_file_path = 'sample.log'
    logger.info(f"Starting log analysis for file: {log_file_path}")

    # Read and parse log file into a DataFrame
    df = read_and_parse_log_file(log_file_path)

    if df.empty:
        logger.error("No log data was parsed. Exiting.")
        return

    # Analyze Requests per IP
    requests_per_ip = analyze_requests_per_ip(df)
    display_results("Requests per IP", requests_per_ip)

    # Analyze Most Accessed Endpoint
    most_accessed_endpoint = analyze_most_accessed_endpoint(df)
    display_results("Most Accessed Endpoint", most_accessed_endpoint)

    # Analyze Suspicious Activity (failed logins)
    suspicious_activity = analyze_suspicious_activity(df)
    display_results("Suspicious Activity", suspicious_activity)

    # Save results to CSV file
    try:
        with open('log_analysis_results.csv', 'w') as f:
            # Write Requests per IP section
            f.write('--- Requests per IP ---\n')
            requests_per_ip.to_csv(f, index=False)

            # Write Most Accessed Endpoint section
            f.write('\n\n--- Most Accessed Endpoint ---\n')
            most_accessed_endpoint.to_csv(f, index=False)

            # Write Suspicious Activity section
            f.write('\n\n--- Suspicious Activity ---\n')
            suspicious_activity.to_csv(f, index=False)
    except Exception as e:
        logger.error(f"Error saving analysis results to file: {e}")


if __name__ == "__main__":
    main()
