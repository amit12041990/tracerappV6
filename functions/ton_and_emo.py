from spellchecker import SpellChecker
import asyncio
import language_tool_python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
import re

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
        '''
        print("Original Comment:", comment)
        print("Misspelled Words:", misspelled_words)
        print("correct words", corrected_wordss)
        print("Corrected Comment:", corrected_comment)
        print("Original Comment:", comment)
        print("Grammar Mistakes:", grammar_mistakes)
        print("Corrections:", corrections)
        print("Words:", words)
        print("Corrected Comment:", corrected_comment)
        '''
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

