import asyncio
import re
import enchant
from language_tool_python import LanguageTool
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from spellchecker import SpellChecker
import language_tool_python
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
from datetime import datetime
#import datetime
from collections import defaultdict






#---------------------------------------
#
#    LANGUAGE ACCURACY USING COMMENTS 
#
#-----------------------------------------------
async def language_accuracy_using_comments2(alldata):
    # Create a list to store the comments
    data = alldata
    comments_set = set()

    for keyword in data["keywords"]:
        for comment_info in keyword.get("comment", []):
            comments_set.add(comment_info["comment"])
    comments_array = list(comments_set)
    filtered_list = []
   

    for item in comments_array:
        # Remove newline and tab characters
        cleaned_item = item.replace('\n', '').replace('\t', '')

        # Filter out HTML-related content
        if re.search(r'<[^>]+>', cleaned_item):
            continue

        filtered_list.append(cleaned_item)
        
     

    # Use asyncio.gather to run the analysis functions concurrently
    grammer, spell, fl_right_imp= await asyncio.gather(
        grammatical_correctness(filtered_list),
        spell_checker(filtered_list),
        analyze_comments(filtered_list)
      
    )
    
    return [grammer, spell, fl_right_imp]

#-------------------------------
   # Function to calculate percentile
def calculate_percentile(value_list, value):
    count = value_list.count(value)
    return (count / len(value_list)) * 100
#-----------------------------------------
async def grammatical_correctness(data):
    comments = data
    # Initialize LanguageTool for grammatical correctness
    tool = LanguageTool('en-US')

    # Variables to keep track of analysis results
    grammatically_correct_count = 0
    total_comments = len(comments)

    for comment in comments:
        # Check grammatical correctness using LanguageTool
        matches = tool.check(comment)
        if len(matches) == 0:
            grammatically_correct_count += 1

    # Calculate percentage of grammatically correct sentences
    grammatically_correct_percentage = (grammatically_correct_count / total_comments) * 100

    return grammatically_correct_percentage

async def spell_checker(data):
    comments = data

    # Initialize enchant spell checker
    spell_checker = enchant.Dict("en_US")

    # Variables to keep track of analysis results
    correctly_spelled_count = 0
    total_comments = len(comments)

    for comment in comments:
        # Check spelling accuracy using enchant spell checker
        doc_words = comment.split()
        misspelled_enchant = [word for word in doc_words if not spell_checker.check(word)]

        if not misspelled_enchant:
            correctly_spelled_count += 1
        else:
            print(f"Misspelled words in '{comment}': {misspelled_enchant}")

    # Calculate percentage of spelling accurate sentences
    spelling_accuracy_percentage = (correctly_spelled_count / total_comments) * 100

    return spelling_accuracy_percentage

async def analyze_comments(data):
    comments = data

    # Initialize sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Variables to keep track of analysis results
    fluent_count = 0
    right_impression_count = 0
    total_comments = len(comments)

    for comment in comments:
        # Check fluency (you can define your own fluency criteria)
        # For demonstration, we'll consider comments with less than 5 words as fluent
        if len(comment.split()) < 5:
            fluent_count += 1

        # Check sentiment and right impression
        sentiment_score = analyzer.polarity_scores(comment)
        if sentiment_score['compound'] >= 0.96:
            right_impression_count += 1

    # Calculate percentages
    fluent_percentage = (fluent_count / total_comments) * 100
    right_impression_percentage = (right_impression_count / total_comments) * 100

    return [fluent_percentage, right_impression_percentage]

#----------------------------------------
#    end of 
#    LANGUAGE ACCURACY USING COMMENTS 
#    use for dashboard render
#--------------------------------------------

#--------------------------------------
#    
#    tonality_emotion_graph_array
#    use for dashboard render
#-----------------------------------------------




nlp = spacy.load("en_core_web_sm")

async def language_accuracy_v1(alldata):
    data=alldata
    comments_set = set()

    for keyword in data["keywords"]:
        for comment_info in keyword.get("comment", []):
            comments_set.add(comment_info["comment"])
    comments_array = list(comments_set)
    comment_array=[]
    for item in comments_array:
        # Remove newline and tab characters
        cleaned_item = item.replace('\n', '').replace('\t', '')
        # Filter out URLs
        #if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', item):
        #    continue
        
         #Filter out HTML-related content
        if re.search(r'<[^>]+>', cleaned_item):
            continue
        
        comment_array.append(cleaned_item)
    
    print(comment_array)
    lang_acc = []
    #comment_array = ["This commmentt has sme speling mistkes .","He is go to the store ."]
    for comment in comment_array:
        misspelled_words, corrected_comment ,corrected_wordss,corrected_words= await analyze_spelling_mistakes(comment)
        grammar_mistakes, corrections, words, corrected_comment =await analyze_grammar_mistakes(comment)
        fluency = await analyze_fluency(comment)
        sentiment = await analyze_sentiment(comment)
        
        lang_acc.append(dict({
            'comment':comment,
            'misspelled_words':misspelled_words if misspelled_words else 0,
            'correct_words' : split_word(comment,corrected_words) if corrected_words else 'ok',
            'grammar_mistakes': str(grammar_mistakes) if grammar_mistakes else 'none',
            'correction': str(corrections) if corrections else 'ok',
            'correct_comment':corrected_comment if corrected_comment else True,
            'fluent':fluency,
            'impression':sentiment
            
            }))
    return lang_acc
        
        
def split_word(comment,arr):
    # Split the string w into words
    split_w = comment.split()

    # Find words in s that are not present in split_w
    result = [word for word in arr if word not in split_w]
    if result:
       return result
    else:
        'no mistake'
           
async def tonality_emotion_graph_array(keywords,need):
        
        print('tonality_emotion_graph_array CALLED')
        seen_comments = set()
        filtered_comments = []
        comments = []
        tonality = []
        emotion = []

        for entry in keywords:
            if 'comment' in entry:
                comment_list = entry['comment']
                for comment_entry in comment_list:
                    comment_text = comment_entry['comment']
                    if comment_text not in seen_comments:
                        seen_comments.add(comment_text)
                        filtered_comments.append(comment_entry)

        print(filtered_comments)
        for each_comment in filtered_comments:
            tonality.append(each_comment['tonality'])  
            emotion.append(each_comment['emotion']) 

        print(tonality)  
        print(emotion) 
         # Calculate unique values and corresponding percentiles for values
        unique_values_ton = []
        unique_percentiles_ton = []

        for value in tonality:
            if value not in unique_values_ton:
                unique_values_ton.append(value)
                percentile = calculate_percentile(tonality, value)
                unique_percentiles_ton.append(percentile)

        # Calculate unique labels and corresponding percentiles for value2
        unique_val_emo = []
        unique_percentiles_emo = []

        for label in emotion:
            if label not in unique_val_emo:
                unique_val_emo.append(label)
                percentile = calculate_percentile(emotion, label)
                unique_percentiles_emo.append(percentile)


        if need=='dashboard':
           return [{'ton':[unique_values_ton,unique_percentiles_ton],'emo':[unique_val_emo,unique_percentiles_emo],'tot_comments':len(filtered_comments)}]
        elif need =='family':
            return filtered_comments
        else: return []
    
       # Function to calculate percentile
def calculate_percentile(value_list, value):
    count = value_list.count(value)
    return (count / len(value_list)) * 100

'''
LANGUAGE ACCURACY 

'''
async def analyze_grammar_mistakes(comment):
    tool = language_tool_python.LanguageTool('en-US')  # Use 'en-US' for English language

    # Find grammar mistakes and get suggestions
    matches = tool.check(comment)

    # Collect grammar mistakes, words, and their corrections
    grammar_mistakes = []
    corrections = {}
    words = {}
    for match in matches:
        grammar_mistakes.append(match.ruleId)
        corrections[match.ruleId] = match.replacements[0] if match.replacements else None

        # Extract words based on mistake's position
        mistake_start = match.offset
        mistake_end = match.offset + match.errorLength
        mistake_word = comment[mistake_start:mistake_end]
        words[match.ruleId] = mistake_word

    corrected_comment = tool.correct(comment)

    return grammar_mistakes, corrections, words, corrected_comment


async def analyze_spelling_mistakes(comment):
    spell = SpellChecker()

    # Tokenize the comment into words
    words = comment.split()

    # Find misspelled words
    misspelled = spell.unknown(words)

    # Correct the misspelled words
    corrected_words = [spell.correction(word) if word in misspelled else word for word in words]
    corrected_comment = ' '.join([word for word in corrected_words if word is not None])
    corrected_wordss = [word for word in words if word in misspelled and spell.correction(word) is not None]

    return misspelled, corrected_comment, corrected_wordss, corrected_words


async def analyze_sentiment(text):
    # Initialize sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Get sentiment score
    sentiment_score = analyzer.polarity_scores(text)['compound']

    # Convert sentiment score to percentage
    sentiment_percentage = (sentiment_score + 1) * 50

    # Return sentiment percentage
    return sentiment_percentage





async def analyze_fluency(text):
    doc = nlp(text)
    
    # For demonstration, we'll consider texts with an average of less than 10 words per sentence as fluent
    total_words = len([token for token in doc if not token.is_punct])
    total_sentences = len(list(doc.sents))
    
    average_words_per_sentence = total_words / total_sentences
    
    fluency_percentage = (average_words_per_sentence / 10) * 100
    if fluency_percentage > 100:
        fluency_percentage = 100
    
    return fluency_percentage

#----------------------------
#    end of
#    tonality_emotion_graph_array
#    use for dashboard render
#----------------------------------------

#--------------------------------
#    
#    SCREEN TIME COUNT
#    use for dashboard render
#-------------------------------------------



def convert_to_iso8601(timestamp):
    date_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    iso8601_timestamp = date_obj.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    return iso8601_timestamp

async def screen_time_count(data):
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
#--------------------------------
#    end of
#    SCREEN TIME COUNT
#    use for dashboard render
#-------------------------------------------

#--------------------------------
#    
#    PAGES DURATION [total pages,total duration]
#    use for dashboard render
#-------------------------------------------
async def pages_duration(data):
    urls = data['urls']
    total_duration=0
    total_pages=0
    for each in urls:
        total_duration+=each['sec']
        total_pages+=1
    return [total_pages,total_duration]
#--------------------------------
#    end of
#    PAGES DURATION [total pages,total duration]
#    use for dashboard render
#-------------------------------------------

#--------------------------------
#    
#    WORD CLOUD 
#    use for dashboard render
#-------------------------------------------
import pandas as pd
async def wcloud (listArr):
    from datetime import datetime
      # Convert 'timestamp' column to datetime
    print(listArr)
# Create an empty list to store modified dictionaries
    modified_listArr = []

# Loop through the dictionaries and check if 'timestamp' key exists
    for item in listArr:
        if 'timestamp' in item:
            # Convert 'timestamp' column to datetime
            item['timestamp'] = item['timestamp'].strftime('%Y-%m-%d %H:%M:%S.%f')
        # Append the modified or unmodified dictionary to the new list
        modified_listArr.append(item)
    result = pd.DataFrame(modified_listArr).groupby('keyword', as_index=False).sum(numeric_only=False).to_dict(orient='records')
    
    return result
#--------------------------------
#    end of
#    WORD CLOUD 
#    use for dashboard render
#------------------------------------------- 

#--------------------------------
#    
#    LANGUAGE ACCURACY V2
#    use for dashboard render
#------------------------------------------- 
nlp = spacy.load("en_core_web_sm")

#for extension use
async def language_accuracy_v2(alldata):
    data=alldata
    comments_set = set()
    print ('language accuracy v2')
    #print(data)
    lang_acc = []
    
    for each in data:
        try:
            comment = each['comment']
            if comment:
                comments_set.add(comment)
        except KeyError:
            # Handle the case where 'comment' key is not present in the dictionary
            return lang_acc
        
    comments_array = list(comments_set)
    
    comment_array=[]
    for item in comments_array:
        # Remove newline and tab characters
        cleaned_item = item.replace('\n', '').replace('\t', '')
        # Filter out URLs
        #if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', item):
        #    continue
        
         #Filter out HTML-related content
        if re.search(r'<[^>]+>', cleaned_item):
            continue
        
        comment_array.append(cleaned_item)
    
    print(comment_array)
    
    #comment_array = ["This commmentt has sme speling mistkes .","He is go to the store ."]
    for comment in comment_array:
        misspelled_words, corrected_comment ,corrected_wordss,corrected_words= await analyze_spelling_mistakes(comment)
        grammar_mistakes, corrections, words, corrected_comment =await analyze_grammar_mistakes(comment)
        fluency = await analyze_fluency(comment)
        sentiment = await analyze_sentiment(comment)
        spell_count = await spell_checker(comment)
        grammer_count = await grammatical_correctness(comment)
       
        lang_acc.append(dict({
            'comment':comment,
            'misspelled_words':misspelled_words if misspelled_words else 0,
            'correct_words' : split_word(comment,corrected_words) if corrected_words else 'ok',
            'grammar_mistakes': str(grammar_mistakes) if grammar_mistakes else 'none',
            'correction': str(corrections) if corrections else 'ok',
            'correct_comment':corrected_comment if corrected_comment else True,
            'fluent':fluency,
            'impression':sentiment,
            'spell_count':spell_count,
            'grammar_count':grammer_count,
            'time':datetime.now()
            
            }))
    return lang_acc
#for exention use ^

async def language_accuracy_v1(alldata):
    data=alldata
    comments_set = set()

    for keyword in data["keywords"]:
        for comment_info in keyword.get("comment", []):
            comments_set.add(comment_info["comment"])
    comments_array = list(comments_set)
    comment_array=[]
    for item in comments_array:
        # Remove newline and tab characters
        cleaned_item = item.replace('\n', '').replace('\t', '')
        # Filter out URLs
        #if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', item):
        #    continue
        
         #Filter out HTML-related content
        if re.search(r'<[^>]+>', cleaned_item):
            continue
        
        comment_array.append(cleaned_item)
    
    print(comment_array)
    lang_acc = []
    #comment_array = ["This commmentt has sme speling mistkes .","He is go to the store ."]
    for comment in comment_array:
        misspelled_words, corrected_comment ,corrected_wordss,corrected_words= await analyze_spelling_mistakes(comment)
        grammar_mistakes, corrections, words, corrected_comment =await analyze_grammar_mistakes(comment)
        fluency = await analyze_fluency(comment)
        sentiment = await analyze_sentiment(comment)
       
        lang_acc.append(dict({
            'comment':comment,
            'misspelled_words':misspelled_words if misspelled_words else 0,
            'correct_words' : split_word(comment,corrected_words) if corrected_words else 'ok',
            'grammar_mistakes': str(grammar_mistakes) if grammar_mistakes else 'none',
            'correction': str(corrections) if corrections else 'ok',
            'correct_comment':corrected_comment if corrected_comment else True,
            'fluent':fluency,
            'impression':sentiment
            
            }))
    return lang_acc
        
        
def split_word(comment,arr):
    # Split the string w into words
    split_w = comment.split()

    # Find words in s that are not present in split_w
    result = [word for word in arr if word not in split_w]
    if result:
       return result
    else:
        'no mistake'
           
async def tonality_emotion_graph_array(keywords,need):
        
        print('tonality_emotion_graph_array CALLED')
        seen_comments = set()
        filtered_comments = []
        comments = []
        tonality = []
        emotion = []

        for entry in keywords:
            if 'comment' in entry:
                comment_list = entry['comment']
                for comment_entry in comment_list:
                    comment_text = comment_entry['comment']
                    if comment_text not in seen_comments:
                        seen_comments.add(comment_text)
                        filtered_comments.append(comment_entry)
            #else:return [{'ton':[['Tonality Not Found'],[[100]]],'emo':[['Emotion Not Found'],[[100]]],'tot_comments':0}]
                
        #print(filtered_comments)
        for each_comment in filtered_comments:
            tonality.append(each_comment['tonality'])  
            emotion.append(each_comment['emotion']) 

        print(tonality)  
        print(emotion) 
         # Calculate unique values and corresponding percentiles for values
        unique_values_ton = []
        unique_percentiles_ton = []

        for value in tonality:
            if value not in unique_values_ton:
                unique_values_ton.append(value)
                percentile = calculate_percentile(tonality, value)
                unique_percentiles_ton.append(percentile)

        # Calculate unique labels and corresponding percentiles for value2
        unique_val_emo = []
        unique_percentiles_emo = []

        for label in emotion:
            if label not in unique_val_emo:
                unique_val_emo.append(label)
                percentile = calculate_percentile(emotion, label)
                unique_percentiles_emo.append(percentile)


        if need=='dashboard':
            for entry in keywords:
                if len(filtered_comments)>0:
                    return [{'ton':[unique_values_ton,unique_percentiles_ton],'emo':[unique_val_emo,unique_percentiles_emo],'tot_comments':len(filtered_comments)},]
                else:return [{'ton':[['Tonality Not Found'],[[100]]],'emo':[['Emotion Not Found'],[[100]]],'tot_comments':0}]
                    
        elif need =='family':
            return filtered_comments
        else: return []
    
       # Function to calculate percentile
def calculate_percentile(value_list, value):
    count = value_list.count(value)
    return (count / len(value_list)) * 100

'''
LANGUAGE ACCURACY 

'''
async def analyze_grammar_mistakes(comment):
    tool = language_tool_python.LanguageTool('en-US')  # Use 'en-US' for English language

    # Find grammar mistakes and get suggestions
    matches = tool.check(comment)

    # Collect grammar mistakes, words, and their corrections
    grammar_mistakes = []
    corrections = {}
    words = {}
    for match in matches:
        grammar_mistakes.append(match.ruleId)
        corrections[match.ruleId] = match.replacements[0] if match.replacements else None

        # Extract words based on mistake's position
        mistake_start = match.offset
        mistake_end = match.offset + match.errorLength
        mistake_word = comment[mistake_start:mistake_end]
        words[match.ruleId] = mistake_word

    corrected_comment = tool.correct(comment)

    return grammar_mistakes, corrections, words, corrected_comment


async def analyze_spelling_mistakes(comment):
    spell = SpellChecker()

    # Tokenize the comment into words
    words = comment.split()

    # Find misspelled words
    misspelled = spell.unknown(words)

    # Correct the misspelled words
    corrected_words = [spell.correction(word) if word in misspelled else word for word in words]
    corrected_comment = ' '.join([word for word in corrected_words if word is not None])
    corrected_wordss = [word for word in words if word in misspelled and spell.correction(word) is not None]

    return misspelled, corrected_comment, corrected_wordss, corrected_words


async def analyze_sentiment(text):
    # Initialize sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Get sentiment score
    sentiment_score = analyzer.polarity_scores(text)['compound']

    # Convert sentiment score to percentage
    sentiment_percentage = (sentiment_score + 1) * 50

    # Return sentiment percentage
    return sentiment_percentage





async def analyze_fluency(text):
    doc = nlp(text)
    
    # For demonstration, we'll consider texts with an average of less than 10 words per sentence as fluent
    total_words = len([token for token in doc if not token.is_punct])
    total_sentences = len(list(doc.sents))
    
    average_words_per_sentence = total_words / total_sentences
    
    fluency_percentage = (average_words_per_sentence / 10) * 100
    if fluency_percentage > 100:
        fluency_percentage = 100
    
    return fluency_percentage

#--------------------
# LANGUAGE ACCURACY PAGE RENDER
#-----------------------
async def lang_acc_map(fetched_data):
    if 'language_accuracy' in fetched_data[0]:
        #print(fetched_data[0]['language_accuracy'])
        return fetched_data[0]['language_accuracy']
    else: 
        return [{'correction':'No Comment Found '}]
#-----------------------
# DASHBOARD  Lang acc chartjs
#---------------------------
async def lang_acc_chart(fetched_data):
    if 'language_accuracy' in fetched_data[0]:
        lang_acc_data = fetched_data[0]['language_accuracy']
        grammer_correct = []
        spell_correct =[]
        fluency = []
        impression =[]
        for item in lang_acc_data:
            grammer_correct.append(item.get('grammer_mistake_count'))
            spell_correct.append(item.get('spell_mistake_count'))
            fluency.append(item.get('fluent'))
            impression.append(item.get('impression'))
        # Now, divide each count by the length of the respective list
        grammer_correct_average = sum(grammer_correct) / len(grammer_correct)
        spell_correct_average = sum(spell_correct) / len(spell_correct)
        fluency_average = sum(fluency) / len(fluency)
        impression_average = sum(impression) / len(impression)
        
        return [grammer_correct_average,spell_correct_average,fluency_average,impression_average,lang_acc_data]
    
    else:
        return [0,0,0,0]
    
    
    
    # For Mobile Comments And Search Query
async def language_accuracy_mobile(alldata):
    data=alldata
    comments_set = set()
    print ('language accuracy v2')
    #print(data)
    lang_acc = []
    
    for each in data:
        try:
            comment = each['comment']
            if comment:
                comments_set.add(comment)
        except KeyError:
            # Handle the case where 'comment' key is not present in the dictionary
            return lang_acc
        
    comments_array = list(comments_set)
    
    comment_array=[]
    for item in comments_array:
        # Remove newline and tab characters
        cleaned_item = item.replace('\n', '').replace('\t', '')
        # Filter out URLs
        #if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', item):
        #    continue
        
         #Filter out HTML-related content
        if re.search(r'<[^>]+>', cleaned_item):
            continue
        
        comment_array.append(cleaned_item)
    
    print(comment_array)
    
    #comment_array = ["This commmentt has sme speling mistkes .","He is go to the store ."]
    for comment in comment_array:
        misspelled_words, corrected_comment ,corrected_wordss,corrected_words= await analyze_spelling_mistakes(comment)
        grammar_mistakes, corrections, words, corrected_comment =await analyze_grammar_mistakes(comment)
        fluency = await analyze_fluency(comment)
        sentiment = await analyze_sentiment(comment)
        spell_count = await spell_checker(comment)
        grammer_count = await grammatical_correctness(comment)
       
        lang_acc.append(dict({
            'comment':comment,
            'misspelled_words':misspelled_words if misspelled_words else 0,
            'correct_words' : split_word(comment,corrected_words) if corrected_words else 'ok',
            'grammar_mistakes': str(grammar_mistakes) if grammar_mistakes else 'none',
            'correction': str(corrections) if corrections else 'ok',
            'correct_comment':corrected_comment if corrected_comment else True,
            'fluent':fluency,
            'impression':sentiment,
            'spell_count':spell_count,
            'grammar_count':grammer_count,
            'time':datetime.now()
            
            }))
    return lang_acc