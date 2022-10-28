def words(sentence) -> str:
    list_words = sentence.split(' ')
    print(list_words)
    word = ''
    count = 0

    for value in list_words:
        how_many = list_words.count(value)
        if how_many > count:
            count = how_many 
            word = value

    print(f'the word that appeared most often is the [{word}] {count} times')

while True:
    sentence = input(str('type a sentence: '))
    words(sentence)