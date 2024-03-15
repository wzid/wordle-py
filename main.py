import random

def main():
    word = ''
    with open('words.txt', 'r') as file:
        # 3102 is the number of words in the file
        # Get a random line number and set the word to the word on that line
        word_line = random.randint(0, 3102)
        word = file.readlines()[word_line].strip()
    
    if word == '':
        print('Error: No word found')
        return
    
    print('The word is:', word)

if __name__ == '__main__':
    main()