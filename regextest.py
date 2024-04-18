import re
from datetime import datetime, timezone, timedelta

data = "{'EPCData': {'EPCLengthBits': 16, 'EPC': b'0027'}, 'LastSeenTimestampUTC': 1697212698330181, 'PhaseAngle': 92.4609375, 'RSSI': -61.0}"

# Split the string based on commas
result = re.split(r',', data)

# Discard the first item
result = result[1:]

# Remove curly braces from the remaining strings
result = [item.replace('{', '').replace('}', '') for item in result]

extracted_data = [item.split(':')[1].strip() for item in result]
# Assuming extracted_data is a list with the timestamp at index 1
timestamp_unix = int(extracted_data[1])
timestamp_unix_seconds = int(timestamp_unix/1000000)

# Convert the timestamp to a datetime object in UTC
timestamp_utc = datetime.fromtimestamp(timestamp_unix_seconds, tz=timezone.utc)

# Convert the UTC time to Eastern Time (ET)
timestamp_et = timestamp_utc.astimezone(timezone(timedelta(hours=-5)))  # -5 hours for ET

# Format the ET timestamp as a human-readable string
formatted_timestamp_et = timestamp_et.strftime('%Y-%m-%d %H:%M:%S %Z')

# Append the formatted timestamp to the extracted_data list
extracted_data.insert(2, formatted_timestamp_et)

def parse_string(data):
    result = re.split(r',', data)

    # Discard the first item
    result = result[1:]

    # Remove curly braces from the remaining strings
    result = [item.replace('{', '').replace('}', '') for item in result]

    extracted_data = [item.split(':')[1].strip() for item in result]
    # Assuming extracted_data is a list with the timestamp at index 1
    timestamp_unix = int(extracted_data[1])
    timestamp_unix_seconds = int(timestamp_unix/1000000)

    # Convert the timestamp to a datetime object in UTC
    timestamp_utc = datetime.fromtimestamp(timestamp_unix_seconds, tz=timezone.utc)

    # Convert the UTC time to Eastern Time (ET)
    timestamp_et = timestamp_utc.astimezone(timezone(timedelta(hours=-5)))  # -5 hours for ET

    # Format the ET timestamp as a human-readable string
    formatted_timestamp_et = timestamp_et.strftime('%Y-%m-%d %H:%M:%S %Z')

    # Append the formatted timestamp to the extracted_data list
    extracted_data.insert(2, formatted_timestamp_et)

    return extracted_data

print(result)

print(extracted_data)