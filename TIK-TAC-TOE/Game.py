#!/usr/bin/env python
# coding: utf-8

# In[1]:




# In[2]:

import os
def display_board(board):     #simple displaying board 
    os.system('cls')
    print (' '+board[7]+' | '+board[8]+' | '+board[9])
    print ('-----------')
    print (' '+board[4]+' | '+board[5]+' | '+board[6])
    print ('-----------')
    print (' '+board[1]+' | '+board[2]+' | '+board[3])


# In[ ]:





# In[3]:


test_board = ['#','X','O','X','O','X','O','X','O','X'] #test
display_board(test_board)


# In[4]:


def player_input():             #take input from user and assign it to tuple 
    marker = ''
    
    while not (marker == 'X' or marker == 'O'):
        marker = input('Player 1: Do you want to be X or O? ').upper()

    if marker == 'X':
        return ('X', 'O')
    else:
        return ('O', 'X')


# In[5]:


player_input()     #test


# In[6]:


def place_marker(board, marker , position):       #allow user to make x and o in desired position
    board[position] = marker


# In[7]:


place_marker(test_board,'X',5)    #test
display_board(test_board)


# In[8]:


def win_check(board,mark):             #checks all winning possiblity
   return ((board[7] == mark and board[8] == mark and board[9] == mark) or
          (board[4] == mark and board[5] == mark and board[6] == mark) or
          (board[1] == mark and board[2] == mark and board[3] == mark) or
          (board[1] == mark and board[4] == mark and board[7] == mark) or
          (board[2] == mark and board[5] == mark and board[8] == mark) or
          (board[3] == mark and board[6] == mark and board[9] == mark) or
          (board[1] == mark and board[5] == mark and board[9] == mark) or
          (board[7] == mark and board[5] == mark and board[3] == mark) )


# In[9]:


win_check(test_board,'X')


# In[10]:


import random          #randomly return who will play first turn
def choose_first():
    choose = random.randint(1,2)
    if choose == 1:
        return 'Player 1'
    else :
        return 'Player 2'


# In[ ]:





# In[11]:


def space_check(board,position):  #returns all position blank 
    return board[position] == ' '


# In[12]:


def full_board_check(board):   #checks all position if its filled or empty
    for i in range(1,10):
        if space_check(board,i):
            return False
    return True
        


# In[13]:


def player_choice(board):        #takes input from user and also checks space on board 
    position = 0
    while position not in [1,2,3,4,5,6,7,8,9] or not space_check(board,position):
        position = int(input("enter position from (1-9): "))
        
    return position


# In[14]:


def replay():     #function for playing again 
     return input('Do you want to play again? Enter Yes or No: ').lower().startswith('y')


# In[ ]:


print ('Welcome welcome welcome!!')
while True:
    the_board = [' ']*10
    player1_marker , player2_marker = player_input() #tuple unpacking
    
    turn = choose_first()
    print (turn +' will go first')
    
    play_game = input ('ready to play?Y or N').lower() #start of game and confirmation from user to start a game
    
    if play_game == 'y':
        game_on = True
    else :
        game_on = False
    
    while game_on:   #game begin 
        
        if turn == 'Player 1':
            #displaying board
            display_board(the_board)
            #input from user mark it on board
            position = player_choice(the_board)
            place_marker(the_board,player1_marker,position)
            
            if win_check (the_board,player1_marker):
                
                display_board(the_board)
                print ("Player 1 WINS!!!")       #condition for winning
                game_on = False
                
            else:
                
                if full_board_check(the_board):
                    display_board(the_board)
                    print ('TIE Game')
                    break
                else:
                    
                    turn = 'Player 2'
                    
        else :
            #player 2 turn
            display_board(the_board)
            position = player_choice(the_board)
            place_marker(the_board,player2_marker,position)
            
            if win_check (the_board,player2_marker):
                display_board(the_board)
                print ("Player 2 WINS!!!")
                game_on = False
            else:
                if full_board_check(the_board):
                    display_board(the_board)
                    print ('TIE Game')
                    break
                else:
                    turn = 'Player 1'
    
    if not replay():
        break


# 

# In[ ]:





# In[ ]:





# In[ ]:
