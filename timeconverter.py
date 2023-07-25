import datetime

def unix_timestamp_to_iso(unix_timestamp):
    try:
        timestamp = int(unix_timestamp)
        # Convert Unix timestamp to a datetime object
        dt_object = datetime.datetime.fromtimestamp(timestamp)

        # Convert datetime object to ISO 8601 formatted string
        iso_format = dt_object.isoformat()
        return iso_format
    except ValueError:
        return "Invalid Unix timestamp"

# Example usage:
unix_timestamp = 1690021968
iso_format_time = unix_timestamp_to_iso(unix_timestamp)
print(iso_format_time)
