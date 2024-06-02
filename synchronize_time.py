import ntplib
import logging
import time

def synchronize_time(exchange, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            client = ntplib.NTPClient()
            response = client.request('pool.ntp.org')
            server_time = response.tx_time
            local_time = exchange.milliseconds()
            time_offset = server_time - local_time
            return int(time_offset)
        except Exception as e:
            logging.error("Failed to synchronize time with NTP server: %s", e)
            retries += 1
            time.sleep(1)  # Wait for a short duration before retrying

    logging.error("Max retries reached. Unable to synchronize time.")
    return 0  # Return 0 offset if synchronization fails
