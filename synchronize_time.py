import ntplib
import time
import logging

# Function to synchronize time with an NTP server
def synchronize_time(ntp_server='time.google.com', max_retries=3, backoff_factor=1):
    client = ntplib.NTPClient()
    retries = 0
    while retries < max_retries:
        try:
            response = client.request(ntp_server)
            offset = response.offset
            logging.info(f"Time synchronized with {ntp_server}. Offset: {offset} seconds")
            return offset
        except ntplib.NTPException as e:
            logging.warning(f"Failed to synchronize time on attempt {retries + 1} with {ntp_server}: {e}")
            retries += 1
            time.sleep(backoff_factor * retries)  # Exponential backoff
    logging.error(f"Max retries ({max_retries}) reached. Unable to synchronize time with {ntp_server}.")
    return 0  # Return 0 offset if synchronization fails

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    offset = synchronize_time()
    print(f"Time offset: {offset} seconds")
