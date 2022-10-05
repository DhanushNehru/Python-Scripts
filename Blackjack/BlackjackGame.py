'''

Welcome to GDB Online.
GDB online is an online compiler and debugger tool for C, C++, Python, Java, PHP, Ruby, Perl,
C#, VB, Swift, Pascal, Fortran, Haskell, Objective-C, Assembly, HTML, CSS, JS, SQLite, Prolog.
Code, Compile, Run and Debug online from anywhere in world.

'''

import random

class Player: # 
    #__init__    
    def __init__(self, inputname , inputage, playerType):
        self.name = inputname 
        self.age = inputage
        self.cards = []
        self.score = 0
        self.money = 100
        self.bet = 10
        self.playerType = playerType
        self.scoreDictionary = {
            '2' : 2,
            '3' : 3,
            '4' : 4,
            '5' : 5,
            '6' : 6,
            '7' : 7,
            '8' : 8,
            '9' : 9,
            '10' : 10,
            'J' : 10,
            'Q' : 10,
            'K' : 10,
            'A' : 11
        }
    
    def playRound():
        #dosomething
        #player 
        pass
        
    def drawCards(self ,inputCard ):
        self.cards.append( inputCard )

    def getScore(self):
        self.score = 0
        for card in self.cards:
            self.score = self.score + self.scoreDictionary[card]
        return self.score
    
class GameBlackJack:
    #__init__    
    def __init__(self, dealer, playerlist):
        self.playerlist = playerlist
        self.dealer = dealer
        self.cardDeck = [] 
        self.genDeck() # 


    def drawCardsRound1(self):
        # playerlist = [player1, player2]
        for i in range(2): 
            for player in self.playerlist:
                cardDrawn = self.drawCard()
                # player
                player.drawCards( cardDrawn )

            # for dealer #cardDrawn = self.cardDeck.pop( randNumber )
            cardDrawn = self.drawCard()
            #  dealer
            self.dealer.drawCards( cardDrawn )

        # cards  human
        for player in self.playerlist:
            if player.playerType == 'human':
                print(player.cards)

    def drawCard(self):
        #randNumber = random.randint(0, 51) 
        randNumber = random.randint(0, len(self.cardDeck)-1 )
        #  card deck cardDeck
        cardDrawn = self.cardDeck.pop( randNumber )
        return cardDrawn

    def drawCardsRound2(self):
        # Loop through AI players
        for player in self.playerlist:
            if player.playerType == 'AI':
                # check player score
                while player.getScore() < 14: 
                    cardDrawn = self.drawCard()
                    player.drawCards( cardDrawn )
            elif player.playerType == 'human':
                userChoice = 'yes'
                while userChoice == 'yes':
                    userChoice = input("Do you want to draw extra card? Answer yes or no : ")
                    if userChoice == 'yes':
                        cardDrawn = self.drawCard()
                        player.drawCards( cardDrawn )
                        print(player.cards)
            
    def playRound3(self):
        #  dealer function 
        #  dealer 14 card
        while self.dealer.getScore() < 14: 
            cardDrawn = self.drawCard()
            self.dealer.drawCards( cardDrawn )
        
        print("dealer.cards" + str(self.dealer.cards))

        for player in self.playerlist:
            if (self.dealer.getScore() <= 21) and (player.getScore() <= 21):
                if self.dealer.getScore() > player.getScore():
                    self.dealer.money = self.dealer.money + player.bet
                    player.money = player.money - player.bet
                    print('dealer wins ' + player.name )
                elif self.dealer.getScore() < player.getScore():
                    self.dealer.money = self.dealer.money - player.bet
                    player.money = player.money + player.bet
                    print('dealer loses '  + player.name )
                else:
                    pass
                    print('dealer draw ' + player.name )

            elif (self.dealer.getScore() <= 21) and (player.getScore() > 21):
                print('dealer wins ' + player.name )
            
            elif (self.dealer.getScore() > 21) and (player.getScore() <= 21):
                print('dealer loses ' + player.name )
                self.dealer.money = self.dealer.money + player.bet
                player.money = player.money - player.bet

            elif (self.dealer.getScore() > 21) and (player.getScore() > 21):
                print('dealer wins ' + player.name )
                player.money = player.money + player.bet
                print('dealer loses '  + player.name )

            if player.playerType == "human":
                print("My Money: " + str(player.money))


    def removeLossers(self):
        i = 0
        for player in self.playerlist:
            if player.money <= 0:
                self.playerlist.pop(i)
            i = i + 1
    
    def refreshPlayerCard(self):
        for player in self.playerlist:
            player.cards = []
        dealer.cards = []
                                          
    def genDeck(self):
        cardType = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        self.cardDeck = []
        for card in cardType:
            self.cardDeck.append(card) 
            self.cardDeck.append(card)
            self.cardDeck.append(card)
            self.cardDeck.append(card)
            #print(cardType)
        #print(self.cardDeck)

# Play        
player1 = Player('chawin', 22, 'human')
player2 = Player('soon', 21, 'AI')
player3 = Player('PAXI', 28, 'AI')
player4 = Player('cactus', 41, 'AI')

dealer = Player('Mc Donald', 78, 'AI')

playerlist = [ player1, player2, player3, player4 ] 

game1 = GameBlackJack( dealer, playerlist )

gameRound = 0

while gameRound < 2:
    print("Round " + str(gameRound + 1))
    game1.genDeck()
    game1.refreshPlayerCard()
    game1.drawCardsRound1()
    game1.drawCardsRound2()
    game1.playRound3()
    game1.removeLossers
    gameRound = gameRound + 1

