import os
import sqlite3
import random
import time

deck = [[2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'],
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'],
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'],
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']]
sub_deck = deck
game = False
new = True
player_name = input('please enter your name:')


class Player:
    def __init__(self, name):
        self.hand = list()
        self.value = 0
        self.cash = 1000
        self.stay = False
        self.fold = False
        self.bet = 0
        self.name = name
        self.key = 0
        self.lost = False
        self.won = False
        self.win_counter = 0
        self.round_counter = 0

    def update(self):
        self.value = 0
        for card in self.hand:
            if card == 'J':
                self.value += 10
            elif card == 'Q':
                self.value += 10
            elif card == 'K':
                self.value += 10
            elif card == 'A':
                self.value += 11
            else:
                try:
                    self.value += card
                except:
                    print(card)
        if self.value > 21 and "A" in self.hand:
            self.value -= 10

    def hit(self):
        global deck
        tempf = random.randint(0, 3)
        temps = random.randint(0, 12)
        holder = deck[tempf]
        card = holder[temps]
        self.hand.append(card)
        self.update()

    def add_bet(self):
        try:
            self.key = int(input('How much do you want to bet?'))
        except:
            print('Bad value. Try again.')
            self.add_bet()
        self.bet += int(self.key * 1.5)

    def folds(self):
        print("You folded. You lost ${}!".format(self.key))
        self.fold = True
        self.lost = True
        self.bet = 0
        self.cash -= self.key
        round_end()

    def stayed(self):
        self.stay = True

    def win(self):
        print('You won the round and gained ${}!'.format(self.bet))
        self.cash += self.bet
        self.won = True
        self.bet = 0
        round_end()

    def lose(self):
        print('You lost the round and lost ${}!'.format(self.key))
        self.cash -= self.key
        self.lost = True
        self.bet = 0
        round_end()

    def draw(self):
        print("It's a draw! all bets are returned.")
        self.cash += self.key
        self.won = True
        round_end()


class Dealer:
    def __init__(self):
        self.hand = list()
        self.value = 0
        self.deal_turn = False
        self.first_value = 0
        self.banter = [["Dealer: Hmm, let's try another one", "Dealer: Lady luck be on my side!", "Dealer: Here we go!",
                        "Dealer: Oh this card's calling me!", "Dealer: Here we go!",
                        "Dealer: Not so sure about this one.."],
                       ["Dealer: I guess luck wasn't on my side tonight",
                        "Dealer: What? how? I put the ace her-.. I mean, damn", "Dealer: Figures..",
                        "Dealer: You earned that one.", "Dealer: Impressive.", "Dealer: Good job.",
                        "Dealer: i'm ruined.", "Dealer: Great round!"],
                       ["Dealer: There was never a doubt!", "Dealer: You lose one, you win one!",
                        "Dealer: Tough luck", "Dealer: That's not good.. for you at least.",
                        "Dealer: Oh i'm on fire tonight!", "Dealer: Could be worse!",
                        "Dealer: You paying cash or credit?"]]

    def update(self):
        if type(self.hand[0]) == int:
            self.first_value = self.hand[0]
        else:
            if self.hand[0] == 'A':
                self.first_value = 11
            else:
                self.first_value = 10
        self.value = 0
        for card in self.hand:
            if card == 'J':
                self.value += 10
            elif card == 'Q':
                self.value += 10
            elif card == 'K':
                self.value += 10
            elif card == 'A':
                self.value += 11
            else:
                try:
                    self.value += card
                except:
                    print(card)
        if self.value > 21 and "A" in self.hand:
            self.value -= 10

    def draw(self):
        global deck
        tempf = random.randint(0, 3)
        temps = random.randint(0, 12)
        holder = deck[tempf]
        card = holder[temps]
        self.hand.append(card)
        self.update()


player = Player(player_name)
dealer = Dealer()


def start():
    player.hit()
    player.hit()
    dealer.draw()
    dealer.draw()
    print('Welcome to BlackJack, {}!\nYou currently have ${}!'.format(player.name, player.cash))
    player.add_bet()


def screen_update():
    os.system('cls')
    if not player.stay:
        print("Dealer's hand: {}, unknown.".format(dealer.first_value))
        print("Total value:", dealer.first_value)
    else:
        print("Dealer's hand: ", end='')
        for var, card in enumerate(dealer.hand):
            if var == dealer.hand[len(dealer.hand) - 1]:
                print(card, end='.')
            else:
                print(card, end=', ')
        print('\nTotal value:', dealer.value)
    print('\n')
    print("Player's hand: ", end='')
    for var, card in enumerate(player.hand):
        if var == len(player.hand) - 1:
            print(card, end='.')
        else:
            print(card, end=', ')
    print('\nTotal value:', player.value)
    print("\t\t********")


def round_end():
    player.hand = []
    player.value = 0
    player.bet = 0
    dealer.hand = []
    dealer.value = 0
    dealer.first_value = 0


def score(player_hand, dealer_hand):
    if dealer_hand > 21:
        in_banter = random.choice(dealer.banter[2])
        print(in_banter)
        player.win()
        player.win_counter += 1
    elif player_hand == dealer_hand:
        print("Oh well.")
        player.draw()
    elif dealer_hand < player_hand < 21:
        in_banter = random.choice(dealer.banter[2])
        print(in_banter)
        player.win()
        player.win_counter += 1
    else:
        in_banter = random.choice(dealer.banter[1])
        print(banter)
        player.lose()
    player.round_counter += 1
    round_end()


def save(win):
    connection = sqlite3.connect('Game.sqlite')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS 
            Data(
                id       INTEGER PRIMARY KEY,
                name     TEXT,
                cash     REAL,
                win_rate REAL
                )
    ''')
    cursor.execute('''INSERT INTO Data (name, cash, win_rate) VALUES (?, ?, ?)''', (player.name, player.cash, win))
    connection.commit()
    cursor.close()


def end_screen():
    if player.cash - 1000 > 1:
        print('You have made:${}!'.format(player.cash - 1000))
    else:
        print('You lost ${}.'.format(abs(player.cash - 1000)))
    print('You won {} rounds out of {}.'.format(player.win_counter, player.round_counter))
    print('Win rate:', float(player.win_counter / player.round_counter * 100))
    print('Saving...')
    save(float(player.win_counter / player.round_counter * 100))


def balance_check():
    global game
    if player.cash < 50:
        in_key = input('You are almost out of cash. load more money?')
        if in_key.lower()[0] == 'y':
            player.cash += 1000
        else:
            game = False
            print('Then you can no longer play.')
            end_screen()


def view_score():
    connection = sqlite3.connect('Game.sqlite')
    cursor = connection.cursor()
    try:
        cursor.execute('''SELECT name, cash, win_rate FROM Data ORDER BY cash DESC''')
        row = cursor.fetchone()
        print('Current highscore is ${} and is held by {} with a win rate of {}! '.format(row[1], row[0], row[2]))
        wait = input('Press enter to continue.')
    except:
        print('No highscore yet!')

    cursor.close()
    main_menu()


def reset_score():
    connection = sqlite3.connect('Game.sqlite')
    cursor = connection.cursor()
    cursor.executescript('''
        DROP TABLE IF EXISTS Data;
        CREATE TABLE IF NOT EXISTS 
            Data(
                id       INTEGER PRIMARY KEY,
                name     TEXT,
                cash     REAL,
                win_rate REAL
                );
''')


def main_menu():
    global game
    print('Blackjack!')
    print('''
    Please enter number.
    1. Start
    2. View highscore.
    3. Reset scores.
    4. Quit
    ''')
    try:
        ins = int(input('>'))
        if ins == 1:
            game = True
        if ins == 2:
            view_score()
        if ins == 3:
            reset_score()
        if ins == 4:
            quit(0)
    except:
        print('Invalid input. Restarting..')
        main_menu()


main_menu()

while game:
    if player.lost or player.won:
        key = input('Would you like to play another round?')
        if key[0].lower() == 'n':
            end_screen()
            break
        else:
            print('Fresh round!')
            player.stay = False
            player.fold = False
            player.lost = False
            new = True
    if new:
        start()
        new = False
    if not player.stay and not player.fold and not player.lost:
        screen_update()
        print("""
        What would you like to do?
        1.Hit
        2.Stay
        3.Fold
        """)
        key = input('>')
        if key.lower() == 'hit' or key.lower() == '1':
            player.hit()
            screen_update()
            if player.value > 21:
                print('Bust!')
                time.sleep(1)
                player.lose()
        elif key.lower() == 'stay' or key.lower() == '2':
            player.stay = True
        elif key.lower() == 'fold' or key.lower() == '3':
            player.folds()
    if player.stay:
        if player.value <= dealer.value < 21:
            rand = random.randint(1, 10)
            if rand > 8:
                print('\n')
                banter = random.choice(dealer.banter[0])
                print(banter)
                dealer.draw()
                screen_update()
                time.sleep(1)
            else:
                pass
        while dealer.value <= player.value <= 21:
            print('\n')
            banter = random.choice(dealer.banter[0])
            print(banter)
            dealer.draw()
            time.sleep(1)
            screen_update()
            if dealer.value >= 21:
                break
        score(player.value, dealer.value)
