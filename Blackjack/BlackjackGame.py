import random

class Player:
    def __init__(self, inputname, inputage, playerType):
        self.name = inputname
        self.age = inputage
        self.cards = []
        self.score = 0
        self.money = 1000  # Initial bankroll
        self.bet = 0
        self.playerType = playerType
        self.scoreDictionary = {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'J': 10,
            'Q': 10,
            'K': 10,
            'A': 11
        }

    def placeBet(self):
        while True:
            try:
                bet = int(input("Enter your bet amount: "))
                if bet < min_bet or bet > max_bet:
                    print("Invalid bet amount. Please enter a bet between", min_bet, "and", max_bet)
                elif bet > self.money:
                    print("You don't have enough money for that bet.")
                else:
                    self.bet = bet
                    break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def playRound(self):
        if self.playerType == 'human':
            while self.score < 21:
                userChoice = input("Do you want to draw extra card? Answer yes or no: ")
                if userChoice.lower() == 'yes':
                    cardDrawn = self.drawCard()
                    self.drawCards(cardDrawn)
                    print(self.cards)
                    self.getScore()
                else:
                    break

    def drawCards(self, inputCard):
        self.cards.append(inputCard)

    def getScore(self):
        self.score = 0
        for card in self.cards:
            self.score += self.scoreDictionary[card]
        return self.score

    def adjustAceValue(self):
        while self.score > 21 and 'A' in self.cards:
            self.score -= 10

class GameBlackJack:
    def __init__(self, dealer, playerlist):
        self.playerlist = playerlist
        self.dealer = dealer
        self.cardDeck = []
        self.genDeck()

    def startRound(self):
        for player in self.playerlist:
            player.placeBet()

    def drawCardsRound1(self):
        for i in range(2):
            for player in self.playerlist:
                cardDrawn = self.drawCard()
                player.drawCards(cardDrawn)

            cardDrawn = self.drawCard()
            self.dealer.drawCards(cardDrawn)

        for player in self.playerlist:
            if player.playerType == 'human':
                print(player.cards)

    def drawCard(self):
        randNumber = random.randint(0, len(self.cardDeck)-1)
        cardDrawn = self.cardDeck.pop(randNumber)
        return cardDrawn

    def drawCardsRound2(self):
        for player in self.playerlist:
            if player.playerType == 'AI':
                while player.getScore() < 14:
                    cardDrawn = self.drawCard()
                    player.drawCards(cardDrawn)
            elif player.playerType == 'human':
                userChoice = 'yes'
                while userChoice == 'yes':
                    userChoice = input("Do you want to draw extra card? Answer yes or no: ")
                    if userChoice == 'yes':
                        cardDrawn = self.drawCard()
                        player.drawCards(cardDrawn)
                        print(player.cards)

    def playRound3(self):
        while self.dealer.getScore() < 14:
            cardDrawn = self.drawCard()
            self.dealer.drawCards(cardDrawn)

        print("dealer.cards: " + str(self.dealer.cards))

        for player in self.playerlist:
            if (self.dealer.getScore() <= 21) and (player.getScore() <= 21):
                if self.dealer.getScore() > player.getScore():
                    self.dealer.money += player.bet
                    player.money -= player.bet
                    print('dealer wins ' + player.name)
                elif self.dealer.getScore() < player.getScore():
                    self.dealer.money -= player.bet
                    player.money += player.bet
                    print('dealer loses ' + player.name)
                else:
                    print('dealer draw ' + player.name)

            elif (self.dealer.getScore() <= 21) and (player.getScore() > 21):
                print('dealer wins ' + player.name)

            elif (self.dealer.getScore() > 21) and (player.getScore() <= 21):
                print('dealer loses ' + player.name)
                self.dealer.money -= player.bet
                player.money += player.bet

            elif (self.dealer.getScore() > 21) and (player.getScore() > 21):
                print('dealer wins ' + player.name)
                player.money += player.bet
                print('dealer loses ' + player.name)

            if player.playerType == "human":
                print("My Money: " + str(player.money))

    def removeLossers(self):
        i = 0
        for player in self.playerlist:
            if player.money <= 0:
                self.playerlist.pop(i)
            i += 1

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

# Set betting limits
min_bet = 5
max_bet = 100

# Players
player1 = Player('George', 22, 'human')
player2 = Player('soon', 21, 'AI')
player3 = Player('PAXI', 28, 'AI')
player4 = Player('cactus', 41, 'AI')

dealer = Player('Mc Donald', 78, 'AI')

playerlist = [player1, player2, player3, player4]

game1 = GameBlackJack(dealer, playerlist)

gameRound = 0

while gameRound < 2:
    print("Round " + str(gameRound + 1))
    game1.startRound()  # Prompt players to place bets
    game1.genDeck()
    game1.refreshPlayerCard()
    game1.drawCardsRound1()
    game1.drawCardsRound2()
    game1.playRound3()
    game1.removeLossers()
    gameRound += 1