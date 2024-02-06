import asyncio
import re
import enchant
from language_tool_python import LanguageTool
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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

# The rest of your code remains unchanged

