import random

colors = ['green', 'blue', 'yellow', 'red', 'white']


class Game:
    def __init__(self, clues, players):

        self.discarded_cards = []
        self.active_cards = {}

        for color in colors:
            self.active_cards[color] = [] # List of cards at that index

        self.time_tokens = 8
        self.fuse_tokens = 3
        self.game_lost = False
        self.clues = clues
        self.players = players
        self.current_player = players[0].number

    # Possible moves during a turn

    def give_hint(self, value, color):  # Pass None for one since only one piece may be given
        if self.time_tokens > 0:
            self.time_tokens -= 1

            if value is None and color is not None or value is not None and color is None:
                if value is None:
                    self.clues.append(Clue(color, None, self.players[self.other_player_number()]))
                if color is None:
                    self.clues.append(Clue(None, value, self.players[self.other_player_number()]))
            else:
                print("Too much or not enough hint information")
            self.change_player()
        else:
            print("No tokens available to give hint")

    def discard(self, player, card_index):
        if self.time_tokens < 8:
            print("Discarding...")
            self.time_tokens += 1
            del player.hand[card_index]
            player.draw(player, _deck)
            self.change_player()
        else:
            print("No tokens available to discard cards")

    def play(self, player, card):

        if card in player.hand:
            if self.active_cards[card.color][-1] is (card.value - 1):
                self.active_cards[card.color].extend(card.value)
            else:
                self.fuse_tokens -= 1
                cur_fuses = 3 - self.fuse_tokens
                print("Play invalid, igniting fuse number " + str(cur_fuses) + "...")
                if cur_fuses is 0:
                    self.game_lost = True
                    print("All fuses have been lit, game is over")
        else:
            print("card not in player's hand")
        self.change_player()

    #

    def change_player(self):
        self.current_player = ((self.current_player + 1) % len(self.players))

    def other_player_number(self):
        return (self.current_player + 1) % len(self.players)


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value


class Clue:
    def __init__(self, color, value, affected_player):
        self.value = value
        self.color = color
        self.affected_player = affected_player
        for i in range(len(affected_player.cards_known)):
            if affected_player.hand[i].color == self.color:
                affected_player.cards_known[i].color = self.color
            if affected_player.hand[i].value == self.value:
                affected_player.cards_known[i].value = self.value


class Player:
    def __init__(self, number):
        self.hand = []
        self.number = number
        self.initial_draw(_deck)
        self.cards_known = [Card(None, None)] * len(self.hand)
        self.hand_size

    def discard(self, card_index):
        if 0 < card_index < len(self.hand):
            del self.hand[card_index]
            del self.cards_known[card_index]
            return
        print("Card not in hand")

    def draw(self, deck):
        new_card = deck.pop()
        self.hand.append(new_card)
        self.cards_known.append(Card(None, None))
        if len(deck) is 0:
            print("One turn remaining, draw pile empty")

    def print_hand(self):
        i = 0
        for card in self.cards_known:
            print("Card at index {0}: ".format(i) + card.color if card.color is not None else "Unknown color - {0}".
                  format(str(card.value)) if card.value is not None else "Unknown value")
            i += 1

    def print_full_hand(self):
        for card in self.hand:
            print(card.color + " - " + str(card.value) + "\n")

    def initial_draw(self, deck):
        for _ in range(self.hand_size):
            self.draw(deck)

    def get_optimal_card_to_play(self):
        pass
        # do something to judge what card should be played.


def create_deck():
    deck_length = 50
    deck = []
    colors = ['green', 'blue', 'yellow', 'red', 'white']
    for color in colors:
        for i in range(10):

            if i is 0 or 1 or 2:
                deck.append(Card(color, 1))
            elif i is 3 or 4:
                deck.append(Card(color, 2))
            elif i is 5 or 6:
                deck.append(Card(color, 3))
            elif i is 7 or 8:
                deck.append(Card(color, 4))
            else:
                deck.append(Card(color, 5))

    if len(deck) is deck_length:
        print("*Deck created successfully*")

    random.shuffle(deck)
    return deck

def calculate_final_score(game):
    score_sum = 0
    for color in colors:
        score_sum += max(game.active_cards[color])
    return score_sum

# Game Loop
_deck = create_deck()  # already shuffled
h = Game([], [Player(0), Player(1)])

while not h.game_lost:
    initial_input = input("Player " + str(h.current_player) + "choose an action: (p)lay, (d)iscard, give (h)int")
    h.players[h.current_player].draw(_deck)
    if initial_input == "P" or initial_input == "p":
        h.players[h.current_player].print_hand()
        card_num = int(input("Pick a card index to play\n"))
        while len(h.players[h.current_player].hand) < card_num or card_num < 0:
            print("bad input")
            card_num = input("Pick a card index to play\n")
        h.play(h.players[h.current_player], card_num)
    elif initial_input == "D" or initial_input == "d":
        h.players[h.current_player].print_hand()
        card_num = int(input("Pick a card index to discard\n"))
        while len(h.players[h.current_player].hand) < card_num or card_num < 0:
            print("bad input")
            card_num = input("Pick a card index to discard\n")
        h.discard(h.players[h.current_player], card_num)
    elif initial_input == "H" or initial_input == "h":
        h.players[h.other_player_number()].print_full_hand()
        type_input = input("Give a hint on (V)alue or (C)olor")
        while type_input != "C" or type_input != "c" or type_input != "V" or type_input != "v":
            print("invalid hint")
            type_input = input("Give a hint on (V)alue or (C)olor")
        if type_input == "C" or type_input == "c":
            color_input = input("green, yellow, red, blue, or white").lower()
            while color_input != "green" or color_input != "yellow" or color_input != "red" or color_input != "blue" or color_input != "white":
                print("invalid color")
                color_input = input("green, yellow, red, blue, or white").lower()
            h.give_hint(None, color_input)
        elif type_input == "V" or type_input == "v":
            value_input = int(input("A number 1 - 5"))
            while value_input > 5 or value_input < 0:
                print("invalid number")
                value_input = int(input("A number 1 - 5"))
            h.give_hint(value_input, None)
    else:
        print("Invalid action\n")
        continue
    h.change_player()
