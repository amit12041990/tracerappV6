from datetime import datetime
from collections import defaultdict

def convert_to_iso8601(timestamp):
    date_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    iso8601_timestamp = date_obj.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    return iso8601_timestamp

def screen_time_count(data):
    screen_time  = data['urls']
   
    # Convert timestamps to datetime objects and calculate the time differences in seconds
    timestamps = [entry['timestamp'] for entry in screen_time]
    timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]
    time_diffs = [(timestamps[i + 1] - timestamps[i]).seconds for i in range(len(timestamps) - 1)]

    # Create the result lists
    seconds = time_diffs
    timestampss = [ts.strftime('%Y-%m-%d %H:%M:%S') for ts in timestamps[:-1]]
    
    timestamp_seconds = defaultdict(int)

    for sec, ts in zip(seconds, timestampss):
        timestamp_seconds[ts] += sec

    result = list(timestamp_seconds.values())
    category = list(timestamp_seconds.keys())

    new_category = []
    for each_cat in category:
        new_category.append(convert_to_iso8601(each_cat))
        
    return [result,new_category]