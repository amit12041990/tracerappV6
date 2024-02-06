import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
import neattext.functions as ntf

# Preprocess data
def preprocess_text(text):
    text = ntf.remove_userhandles(text)
    text = ntf.remove_stopwords(text)
    return text

# Train emotion analysis model
def train_emotion_model(filename):
    df = pd.read_csv(filename)
    df['Clean_Text'] = df['Text'].apply(preprocess_text)

    X_features = df['Clean_Text']
    y_labels = df['Emotion']

    x_train, x_test, y_train, y_test = train_test_split(X_features, y_labels, test_size=0.3, random_state=42)

    tfidf = TfidfVectorizer()
    x_train_tfidf = tfidf.fit_transform(x_train)
    x_test_tfidf = tfidf.transform(x_test)

    lr = LogisticRegression(max_iter=5000)
    lr.fit(x_train_tfidf, y_train)

    return lr, tfidf

emotion_model, tfidf_model = train_emotion_model('static/dataset/emotion.csv')

# Analyze user emotion input
async def analyze_emotion(user_input):
    user_input_tfidf = tfidf_model.transform([user_input])
    prediction = emotion_model.predict(user_input_tfidf)
    return emo_ji(prediction[0])

# Train tonality analysis model
def train_tonality_model(filename):
    df = pd.read_csv(filename)
    df['Clean_Text'] = df['Text'].apply(preprocess_text)

    X_features = df['Clean_Text']
    y_labels = df['Tonality']

    x_train, x_test, y_train, y_test = train_test_split(X_features, y_labels, test_size=0.3, random_state=42)

    pipe_lr = Pipeline(steps=[('cv', CountVectorizer()), ('lr', LogisticRegression())])
    pipe_lr.fit(x_train, y_train)

    return pipe_lr

tonality_model = train_tonality_model('static/dataset/tonality.csv')

# Analyze user tonality input
async def analyze_tonality(user_input):
    print('analyze_tonality called')
    prediction = tonality_model.predict([user_input])
    return prediction

# Map emotion to emoji
def emo_ji(mood):
    mood_mapping = {
        "joy": "😄 JOY",
        "sadness": "😢 SAD",
        "fear": "😨 FEAR",
        "anger": "😡 ANGER",
        "surprise": "😮 SURPRISE",
        "neutral": "😐 NEUTRAL",
        "disgust": "🤢 DISGUST",
        "shame": "😳 SHAME"
    }
    return mood_mapping.get(mood.lower(), "❓")

# Usage
'''
user_input = "looking Good and amazing"
emotion_result = analyze_emotion(user_input)
tonality_result = analyze_tonality(user_input)

print("Emotion:", emotion_result)
print("Tonality:", tonality_result)
'''
