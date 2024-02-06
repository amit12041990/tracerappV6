import datetime

def get_date_time_now():
    current_datetime = datetime.datetime.now()

    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_datetime

def format_date_time(d):
    input_datetime = d
    # Parse the input datetime string
    parsed_datetime = datetime.datetime.strptime(input_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Format the datetime in the desired format
    formatted_datetime = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_datetime
