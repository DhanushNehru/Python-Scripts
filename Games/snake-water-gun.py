import random
user = 0
computer = 0
turn = 0
rounds=int(input('enter the number of rounds: '))
while (turn<rounds):
    a = ['Snake','Water','Gun']
    pc = random.choice(a)
    turn +=1
    dic = {1:'Snake',2:'Water',3:'Gun'}
    print('enter a number of your choice')
    b = int(input('1.Snake,2.Water,3.Gun '))
    print("computer's choice " + pc)
    if b in dic:
        print("user's choice " +dic[b])
        if pc == 'Snake':
            if dic[b] == 'Snake':
                print('its tie')
            elif dic[b] == 'Water':
                print('PC wins')
                computer +=1
            elif dic[b] == 'Gun':
                print('user wins')
                user+=1
                
        elif pc == 'Water':
            if dic[b] == 'Snake':
                print('user wins')
                user+=1
            elif dic[b] == 'Water':
                print('its tie')
            elif dic[b] == 'Gun':
                print('computer wins')
                computer +=1
        elif pc == 'Gun':
            if dic[b] == 'Snake':
                print('PC wins')
                computer+=1
            elif dic[b] == 'Water':
                print('user wins')
                user+=1
            elif dic[b] == 'Gun':
                print('its a tie')
    else:
        print('retry entry')

print('Game over', 'user:',user,'computer:',computer)