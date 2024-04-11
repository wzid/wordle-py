from datetime import date

# Y - M - D
first_day = date(2024, 4, 8)

today = date.today()

def get_word_of_day() -> str:
    word = ''
    with open('word-storage/words.txt', 'r') as file:
        """
        3102 is the number of words in the file
        Get a word from the file based on the current day.
        A word should not repeat for 3103 days.
        """
        word_index = (today - first_day).days % 3103

        word = file.readlines()[word_index].strip()
    
    return word