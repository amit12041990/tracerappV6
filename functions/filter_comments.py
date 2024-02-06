import re
from functions.check_emo_ton import *

async def comments_filter(alldata):
    data=alldata
    comments_set = set()

    for keyword in data["keywords"]:
        for comment_info in keyword.get("comment", []):
            comments_set.add(comment_info["comment"])
    comments_array = list(comments_set)
    commnet_length = len(comments_array)
    filtered_list=[]
    filtered_list2=[]
    for item in comments_array:
        # Remove newline and tab characters
        cleaned_item = item.replace('\n', '').replace('\t', '')
        # Filter out URLs
        #if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', item):
        #    continue
        
         #Filter out HTML-related content
        if re.search(r'<[^>]+>', cleaned_item):
            continue
        filtered_list.append(cleaned_item)
    for each in filtered_list:
        filtered_list2.append({'comment':each})
    
    for each in filtered_list2:
                    scores = userTonality(each['comment'],'static/dataset/tonality.csv')
                    emotion =analysis(each['comment'],'static/dataset/emotion.csv')
                    '''
                    # Determine the tonality based on the compound score
                    compound_score = scores['compound']

                    if compound_score >= 0.05:
                        tonality = "Positive"
                    elif compound_score <= -0.05:
                        tonality = "Negative"
                    else:
                        tonality = "Neutral"
                    '''
                    each['ton'] = scores
                    each['emo'] = emotion   
       
           
    
        
    print('comment filter function') 
    
    #print(filtered_list2)
    ton_val=[]
    emo_val=[]
    for every in filtered_list2:
        ton_val.append(every['ton'][0])
        emo_val.append(every['emo'])
    
    # Calculate unique values and corresponding percentiles for values
    unique_values_ton = []
    unique_percentiles_ton = []

    for value in ton_val:
        if value not in unique_values_ton:
            unique_values_ton.append(value)
            percentile = calculate_percentile(ton_val, value)
            unique_percentiles_ton.append(percentile)

    # Calculate unique labels and corresponding percentiles for value2
    unique_val_emo = []
    unique_percentiles_emo = []

    for label in emo_val:
        if label not in unique_val_emo:
            unique_val_emo.append(label)
            percentile = calculate_percentile(emo_val, label)
            unique_percentiles_emo.append(percentile)


    
    return [{'ton':[unique_values_ton,unique_percentiles_ton],'emo':[unique_val_emo,unique_percentiles_emo],'tot_comments':commnet_length}]

   # Function to calculate percentile
def calculate_percentile(value_list, value):
    count = value_list.count(value)
    return (count / len(value_list)) * 100