import random
array = []
with open('../words-alpha.txt', 'r') as file:
    array = file.readlines()

array = [word.strip() for word in array]

shuffled_list = sorted(array, key=lambda x: random.random())

with open('../words.txt', 'w') as file:
    for word in shuffled_list:
        file.write(word + '\n')