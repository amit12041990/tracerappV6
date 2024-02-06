import nltk
nltk.download('veder_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    # Initialize sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Get sentiment score
    sentiment_score = analyzer.polarity_scores(text)['compound']

    # Convert sentiment score to percentage
    sentiment_percentage = (sentiment_score + 1) * 50

    # Return sentiment percentage
    return sentiment_percentage

# Example usage
text = "I'm really excited about this project. It's going to be amazing!"
sentiment_percent = analyze_sentiment(text)

print("Sentiment Score Percentage:", sentiment_percent, "%")

import spacy

nlp = spacy.load("en_core_web_sm")

def analyze_fluency(text):
    doc = nlp(text)
    
    # For demonstration, we'll consider texts with an average of less than 10 words per sentence as fluent
    total_words = len([token for token in doc if not token.is_punct])
    total_sentences = len(list(doc.sents))
    
    average_words_per_sentence = total_words / total_sentences
    
    fluency_percentage = (average_words_per_sentence / 10) * 100
    if fluency_percentage > 100:
        fluency_percentage = 100
    
    return fluency_percentage

# Example usage
text = "This is a short example sentence. It's easy to understand."
fluency_percent = analyze_fluency(text)

print("Fluency Percentage:", fluency_percent, "%")


