from datetime import datetime
from pymongo import MongoClient

# Establish a connection to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# Access the desired database and collection
db = client['childTrace']
collection = db['members']

# Define the input datetime and ref_id values
def fetch_screen_using_timestamp(childID):
    print ('function called')
    print(childID)
    
    
    data = collection.find_one({'u_id':childID})
    print(data)
    all_urls = data['urls']
   # print(all_urls)
    original_data = [
        {'sec': 392, 'url': 'https://chat.openai.com/', 'timestamp': '2023-08-21 09:36:54'},
        {'sec': 575, 'url': 'https://stackoverflow.com/questions/20019958/chrome-extension-how-to-send-data-from-content-script-to-popup-html', 'timestamp': '2023-08-21 09:36:54'},
        # ... and so on for the rest of the data
    ]

    # Convert the original data to the desired structure
    table_data = []
    for entry in all_urls:
        date, time = entry['timestamp'].split()
        total_time = entry['sec']
        url_entry = {
            "Time": time,
            "URL": entry['url'],
            "Total Time": total_time
        }

        found_date = False
        for date_entry in table_data:
            if date_entry["Date"] == date:
                date_entry["URLs"].append(url_entry)
                date_entry["Total URLs"] += 1
                date_entry["Total Time"] += total_time
                found_date = True
                break

        if not found_date:
            new_date_entry = {
                "Date": date,
                "URLs": [url_entry],
                "Total URLs": 1,
                "Total Time": total_time
            }
            table_data.append(new_date_entry)

    print(table_data)
    return table_data






   
    
   

    
