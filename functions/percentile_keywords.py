import numpy as np

# Your server data
def word_cloud_list_2(data):
    print(data[0])
    server_data=data
    server_datas = [{
        "comment": [
{
"comment": "Ram siya Ram , Siya ram , jai jai ram",
"date": "8/13/2023, 6:44:13 AM",
"title": "Ram Siya Ram  | Lofi Version | Mangal Bhavan Amangal Hari | राम सिया राम | 1 hour straight | - YouTube",
"url": "https://www.youtube.com/watch?v=FIeJs8aeR3Y"
},
{
"comment": "mere tan man siya ram ram hai ",
"date": "8/13/2023, 6:44:39 AM",
"title": "Ram Siya Ram  | Lofi Version | Mangal Bhavan Amangal Hari | राम सिया राम | 1 hour straight | - YouTube",
"url": "https://www.youtube.com/watch?v=FIeJs8aeR3Y"
},
{
"comment": "mere tan man siya ram ram hai <img class=\"emoji yt-formatted-string\" src=\"https://yt3.ggpht.com/5RDrtjmzRQKuVYE_FKPUHiGh7TNtX5eSNe6XzcSytMsHirXYKunxpyAsVacTFMg0jmUGhQ=w24-h24-c-k-nd\" alt=\"face-purple-wide-eyes\" data-emoji-id=\"UCkszU2WH9gy1mb0dV-11UJg/DfgfY9LaNdmMq7IPuI2AaA\">",
"date": "8/13/2023, 6:44:47 AM",
"title": "Ram Siya Ram  | Lofi Version | Mangal Bhavan Amangal Hari | राम सिया राम | 1 hour straight | - YouTube",
"url": "https://www.youtube.com/watch?v=FIeJs8aeR3Y"
}
],
"keyword": "SIYARAM",
"pages": 4,
"sec": 221,
"video": 1,
"video_url": [
"https://www.youtube.com/watch?v=FIeJs8aeR3Y"
]

       
        # Add more data here
   } ]

    # Calculate percentiles based on "sec" values
    sec_values = [entry["sec"] for entry in server_data]
    percentiles_to_calculate = list(range(5, 100, 5))  # [5, 10, 15, ..., 95]
    percentiles = np.percentile(sec_values, percentiles_to_calculate)

    # Calculate percentiles and add them to the list
    result_list = []
    for entry in server_data:
        sec = entry["sec"]
        percentile_value = None

        for p in percentiles_to_calculate:
            if sec <= np.percentile(sec_values, p):
                percentile_value = p
                break
     
       
        
        result_list.append([
            entry["keyword"],
            percentile_value,
            'https://www.lipsum.com/',
            entry["sec"],entry["pages"]
            
            ])
   # print(result_list)
    print(result_list)
    return result_list

def filterList(data):
        # Your input list
    input_list = data
    # Your input list


    # Filter out similar keywords and keep only the shortest ones
    filtered_list = []
    seen_keywords = set()

    def is_similar(keyword1, keyword2):
        return keyword1.lower() in keyword2.lower() or keyword2.lower() in keyword1.lower()

    for item in input_list:
        keyword = item[0]

        # Check if the keyword is a grammatical word or matches certain criteria
        ignore_keywords = ['how', 'howto', 'why', 'which']  # Add more as needed
        if keyword.lower() in ignore_keywords:
            continue
        
        # Check if the keyword is similar to any already seen keywords
        is_duplicate = any(is_similar(keyword, seen_keyword) for seen_keyword in seen_keywords)
        
        # If not a duplicate, add the keyword to the filtered list and the set of seen keywords
        if not is_duplicate:
            # Check if the keyword is a subset of any already seen keyword
            is_subset = any(keyword in seen_keyword.lower() for seen_keyword in seen_keywords)
            if not is_subset:
                filtered_list.append(item)
                seen_keywords.add(keyword)

    return filtered_list
