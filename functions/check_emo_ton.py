import pandas as pd
import emoji
import neattext.functions as ntf
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix


def analysis(user_input, filename):
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
def userTonality(user_input,filename):
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