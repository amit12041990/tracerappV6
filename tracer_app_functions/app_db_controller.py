from datetime import datetime
from pymongo import MongoClient
import pymongo
import asyncio
from decouple import config


# Load configuration from .env
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
MONGO_URI = config('MONGO_URI')
DB_NAME = config('DB_NAME')

# Initialize your MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db['members']

def findAllChild(parrentID):
    try:
        data = db.collection.find({'ref_id',parrentID})
        return data
    except pymongo.errors.PyMongoError as ex:
        print(ex)
        
        

async def fetch_data_using_id(user_id, type):
    try:
        if user_id is None or type not in ['u_id', 'ref_id']:
            return 'Please provide a valid user_id and type (u_id or ref_id).'

        query = {'u_id': user_id} if type == 'u_id' else {'ref_id': user_id}
        
        # Use asyncio.to_thread to run the synchronous MongoDB query in a separate thread
        data = await asyncio.to_thread(collection.find, query)
        
        # Convert the cursor to a list of dictionaries
        data = list(data)
        
        if data:
            return data
        else:
            return [{'gender':'<h4 style="color: #117a65;  padding: 10px;">No Child Created Yet.</h4>'}]
    except pymongo.errors.PyMongoError as ex:
        print(ex)
        return f"Error: {ex}"



        
    
    
# Define the input datetime and ref_id values
async def fetch_screen_TIME_using_timestamp(all_DATA):
    
    
    all_urls = all_DATA
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

    #print(table_data)
   
    return [table_data]