from language_tool_python import LanguageTool
import enchant
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re


def language_accuracy_using_comments(alldata):
    # Create a list to store the comments
    data=alldata
    comments_set = set()

    for keyword in data["keywords"]:
        for comment_info in keyword.get("comment", []):
            comments_set.add(comment_info["comment"])
    comments_array = list(comments_set)
    filtered_list=[]
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
    
    print(filtered_list)
    lang_acc=list()
    lang_acc.append(grammatical_correctness(filtered_list))
    lang_acc.append(spell_checker(filtered_list))
    
    [fluent_percent,right_imp]=analyze_comments(filtered_list)
    lang_acc.append(fluent_percent)
    lang_acc.append(right_imp)
    
    #calculate language accuracy 
    weight_grammar = 0.4  # Increased weight
    weight_spell_check = 0.4  # Increased weight
    weight_fluent = 0.2  # Reduced weight
    total_weight = weight_grammar + weight_spell_check 

    language_accuracy = (weight_grammar * lang_acc[0] + weight_spell_check * lang_acc[1] ) / total_weight

    #print("Language Accuracy:", language_accuracy)
    #print(lang_acc)
    lang_acc.append(language_accuracy)
    return lang_acc


def grammatical_correctness(data):
        comments=data
      
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

        # Print analysis result
       
        return grammatically_correct_percentage

def spell_checker(data):
    comments=data

   

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

    # Print analysis result
    
    return spelling_accuracy_percentage
    
def analyze_comments(data):
    comments=data


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

    # Print analysis results
  
    return [fluent_percentage,right_impression_percentage]






