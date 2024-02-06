from datetime import datetime
from pymongo import MongoClient
import asyncio
import re
import enchant
from language_tool_python import LanguageTool
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import pandas as pd
import emoji
import neattext.functions as ntf
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

# Establish a connection to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# Access the desired database and collection
db = client['childTrace']
collection = db['members']


async def comments_filter(filtered_list):
    filtered_list2 = []
    for each in filtered_list:
        filtered_list2.append({'comment':each})
    
    for each in filtered_list2:
                    scores = await userTonality(each['comment'],'static/dataset/tonality.csv')
                    emotion =await analysis(each['comment'],'static/dataset/emotion.csv')
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


    
    return [{'ton':[unique_values_ton,unique_percentiles_ton],'emo':[unique_val_emo,unique_percentiles_emo],'tot_comments':len(filtered_list2)}]

   # Function to calculate percentile
def calculate_percentile(value_list, value):
    count = value_list.count(value)
    return (count / len(value_list)) * 100

async def language_accuracy_using_comments2():
    # Create a list to store the comments
    child_id ='c8f5010b-7f6d-4da2-a692-ff7bb87a55fe'
    alldata = collection.find_one({'u_id':child_id})
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
    s = time.perf_counter()
    gr = await grammatical_correctness(filtered_list)
    sl = await spell_checker(filtered_list)
    an= await analyze_comments(filtered_list)
    ton = await comments_filter(filtered_list)
    print(gr)
    print(sl)
    print(an)
    print(ton)
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
     

 

#-------------------------------
   # Function to calculate percentile
def calculate_percentile(value_list, value):
    count = value_list.count(value)
    return (count / len(value_list)) * 100

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

#SPELL CHECKER
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

#ANALYZE COMMENTS
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

#TONALITY ANALYSIS
async def analysis(user_input, filename):
    # Load the CSV data into a DataFrame
    df = pd.read_csv(filename)

    # Counting the value of emotions
    result = df['Emotion'].value_counts()
    #print(result)

    # Preprocessing
    df['Clean_Text'] = df['Text'].apply(ntf.remove_userhandles)
    df['Clean_Text'] = df['Clean_Text'].apply(ntf.remove_stopwords)

    # Features and Labels
    X_features = df['Clean_Text']
    y_labels = df['Emotion']

    # Split the data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(X_features, y_labels, test_size=0.3, random_state=42)

    # Vectorization (TF-IDF)
    tfidf = TfidfVectorizer()
    x_train_tfidf = tfidf.fit_transform(x_train)
    x_test_tfidf = tfidf.transform(x_test)

    # Logistic Regression model
    lr = LogisticRegression(max_iter=5000)

    # Train the model
    lr.fit(x_train_tfidf, y_train)

    # Predict on the test set
    y_pred = lr.predict(x_test_tfidf)

    # Calculate evaluation metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    classification_rep = classification_report(y_test, y_pred)
    confusion_mat = confusion_matrix(y_test, y_pred)

    '''
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1-score:", f1)
    print("Classification Report:\n", classification_rep)
    print("Confusion Matrix:\n", confusion_mat)

    '''

    # Predict user input
    user_input_tfidf = tfidf.transform([user_input])
    prediction = lr.predict(user_input_tfidf)
    return emo_ji(prediction[0])





#this function can for Tonality
async def userTonality(user_input,filename):
      #Collecting Csv Data Into Dataframe
    df = pd.read_csv(filename)
    df.head()

    data = []
    #counting Value of emotions
    result= df['Tonality'].value_counts()
    #print(result)
    data.append(result)
    ntx=dir(ntf)
    # User handles
    df['Clean_Text'] = df['Text'].apply(ntf.remove_userhandles)

    # Stopwords
    df['Clean_Text'] = df['Clean_Text'].apply(ntf.remove_stopwords)

    # Features & Labels
    Xfeatures = df['Clean_Text']
    ylabels = df['Tonality']

    #  Split Data
    x_train,x_test,y_train,y_test = train_test_split(Xfeatures,ylabels,test_size=0.3,random_state=42)

    #LogisticRegression Pipeline
    pipe_lr = Pipeline(steps=[('cv',CountVectorizer()),('lr',LogisticRegression())])

    # Train and Fit Data
    pipe_lr.fit(x_train,y_train)

    # Check Accuracy
    checkAc=pipe_lr.score(x_test,y_test)
    #print(checkAc)
    data.append(checkAc)
    data.append(pipe_lr.predict([user_input]))
    return pipe_lr.predict([user_input])

def emo_ji(mood):
    if mood.lower() == "joy":
        return "JOY : 😄"  # Smiling Face with Open Mouth and Smiling Eyes
    elif mood.lower() == "sadness":
        return "SADNESS : 😢"  # Crying Face
    elif mood.lower() == "fear":
        return "FEAR : 😨"  # Fearful Face
    elif mood.lower() == "anger":
        return "ANGER : 😡"  # Pouting Face
    elif mood.lower() == "surprise":
        return "SURPRISE : 😮"  # Face with Open Mouth
    elif mood.lower() == "neutral":
        return "NEUTRAL : 😐"  # Neutral Face
    elif mood.lower() == "disgust":
        return "DISGUST : 🤢"  # Nauseated Face
    elif mood.lower() == "shame":
        return "SHAME : 😳"  # Flushed Face

    else:
        return " NO IDEA : ❓"  # Question Mark