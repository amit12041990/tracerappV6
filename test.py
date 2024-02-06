import enchant

def spell_checker(data):
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

# Example usage
comments_data = ["This is a correctly spelled sentence.", "Thiss is an incorrect sentence with misspellings."]
result = spell_checker(comments_data)
print(f"Spelling accuracy: {result}%")
