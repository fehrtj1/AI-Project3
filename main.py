

class Game:
    def __init__(self, deck, clues, players):

        self.deck = deck
        self.discarded_cards = []
        self.active_cards = {}

        self.time_tokens = 8
        self.fuse_tokens = 3
        self.game_lost = False
        self.clues = []
        self.players = players

    def turn(self, player, action_number):

        if action_number is 0:  # Give one piece of information
            self.time_tokens -= 1

        elif action_number is 1:  # Discard a card
            self.time_tokens += 1
            self.discard(self, player, )

        elif action_number is 2:  # Play a card


            self.play(self, player, player.get_optimal_card())

        else:
            print("Not a valid action")

    def discard(self, player, card):
        print("Discarding...")
        player.discard(card)
        player.draw(Player, self.deck)

    def play(self, player, card):

        if card in player.hand:
            if self.active_cards[card.color][-1] is (card.value - 1):
                self.active_cards[card.color].extend(card.value)
            else:
                self.fuse_tokens -= 1
                cur_fuses = 3 - self.fuse_tokens
                print("Play invalid, igniting fuse number " + cur_fuses + "...")
                if cur_fuses is 0:
                    self.game_lost = True
                    print("All fuses have been lit, game is over")
        else:
            print("card not in player's hand")


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value


class Clue:
    def __init__(self, color, value, positions, affected_player):
        self.value = value
        self.color = color
        self.positions = positions
        self.affected_player = affected_player



class Player:

    def __init__(self, hand):
        self.hand = hand

    def discard(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return
        print("ERR: Card not in hand")

    def draw(self, deck):
        new_card = deck.pop()
        self.hand.append(new_card)
        if len(deck) is 0:
            print("One turn remaining, draw pile empty")

    def get_optimal_card(self):
        pass
        # do something to judge what card should be played.

def create_deck():
    deck_length = 50
    deck = []
    colors = ['green', 'blue', 'yellow', 'red', 'white']

    for color in colors:
        for i in range(10):

            if i is 0 or i is 1 or i is 2:
                deck.append(Card(color, 1))
            elif i is 3 or i is 4:
                deck.append(Card(color, 2))
            elif i is 5 or i is 6:
                deck.append(Card(color, 3))
            elif i is 7 or i is 8:
                deck.append(Card(color, 4))
            else:
                deck.append(Card(color, 5))

    if len(deck) is deck_length:
        print("*Deck created successfully*")

    return deck



######### Game Loop

deck = create_deck()
for card in deck:
    print(str(card.color) + " " + str(card.value))
#hanabi = Game




#while not



