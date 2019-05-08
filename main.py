import random

colors = ['green', 'blue', 'yellow', 'red', 'white']

class Game:
    def __init__(self, clues, players):

        self.discarded_cards = []
        self.active_cards = {}

        for color in colors:
            self.active_cards[color] = []  # List of cards at that index

        self.time_tokens = 8
        self.fuse_tokens = 3
        self.game_lost = False
        self.clues = clues
        self.players = players
        self.current_player = players[0].number
        self.last_turn = False

    # Possible moves during a turn

    def give_hint(self, player, value, color):  # Pass None for one since only one piece may be given
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
            return True
        else:
            print("No tokens available to give hint")
            return False

    def discard(self, player, card_index):
        if self.time_tokens < 8:
            print("Discarding...")
            self.time_tokens += 1
            player.hand[card_index] = None
            player.draw(player, _deck)
            self.change_player()
        else:
            print("No tokens available to discard cards")

    # player = one playing the card
    # card_index = which card in player hand
    # pile = where to play that card, is a color
    def play(self, player, card_index, pile):

        if card_index in range(5):

            # if the card being played is one greater than the last card on that pile,
            # AND they're the same color, we play it
            if self.active_cards[pile][-1].value is player.hand[card_index].value - 1 and pile is player.hand[card_index].color:
                self.active_cards[pile].extend(player.hand[card_index])
            else:
                self.fuse_tokens -= 1
                cur_fuses = 3 - self.fuse_tokens
                print("Play invalid: either value or color does not follow\nIgniting fuse number " + str(cur_fuses) + "...")
                if cur_fuses is 0:
                    self.game_lost = True
                    print("All fuses have been lit, game is over")
        else:
            print("card not in player's hand")
        self.change_player()

    def discard(self, player, card_index):
        if 0 < card_index < len(player.hand):
            player.hand[card_index] = None
            player.cards_known[card_index] = None
            return
        print("Card not in hand")

    def draw(self, player):
        new_card = _deck.pop()

        for card in player.hand:
            if card is None:
                self.hand[self.hand.index(None)] = new_card

        self.cards_known.append(Card(None, None))
        if len(_deck) is 0:
            print("One turn remaining, draw pile empty")
            self.last_turn = True

    #

    def change_player(self):
        self.current_player = ((self.current_player + 1) % len(self.players))

    def other_player_number(self):
        return (self.current_player + 1) % len(self.players)


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return self.color + " - " + str(self.value)


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
        self.cards_known = []
        self.number = number
        self.hand_size = 5
        self.initial_draw(_deck)

    def print_hand(self):
        i = 0
        for card in self.cards_known:
            print("Card at index " + str(i) + ": " +
                  card.color if card.color is not None else "Unknown color - " + str(card.value) if card.value is not None else "Unknown value")
            i += 1

    def print_full_hand(self):
        for card in self.hand:
            print(card.color + " - " + str(card.value) + "\n")

    # Draw 5 at the start of the game
    def initial_draw(self):
        for _ in range(self.hand_size):
            _deck.pop()



def create_deck():
    deck_length = 50
    deck = []
    for color in colors:
        for i in range(10):
            if i == 0 or i == 1 or i == 2:
                deck.append(Card(color, 1))
            elif i == 3 or i == 4:
                deck.append(Card(color, 2))
            elif i == 5 or i == 6:
                deck.append(Card(color, 3))
            elif i == 7 or i == 8:
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
    h.players[h.current_player].draw(_deck)
    initial_input = input("Player " + str(h.current_player) + " choose an action: (p)lay, (d)iscard, give (h)int\n")
    if initial_input.lower() == "p":
        print("Playing a card")
        h.players[h.current_player].print_hand()
        card_num = int(input("Pick a card index to play\n"))
        while len(h.players[h.current_player].hand) < card_num or card_num < 0:
            print("bad input")
            card_num = input("Pick a card index to play\n")
        h.play(h.players[h.current_player], card_num)
    elif initial_input.lower() == "d":
        print("Discarding a card")
        h.players[h.current_player].print_hand()
        card_num = int(input("Pick a card index to discard\n"))
        while len(h.players[h.current_player].hand) < card_num or card_num < 0:
            print("bad input")
            card_num = input("Pick a card index to discard\n")
        h.discard(h.players[h.current_player], card_num)
    elif initial_input.lower() == "h":
        print("Giving a hint")
        h.players[h.other_player_number()].print_full_hand()
        type_input = input("Give a hint on (V)alue or (C)olor\n")
        hint_types = ['c', 'v']
        while type_input.lower() not in hint_types:
            print("\ninvalid hint\n")
            type_input = input("Give a hint on (V)alue or (C)olor\n")
        if type_input.lower() == "c":
            color_input = input("green, yellow, red, blue, or white\n").lower()
            while color_input not in colors:
                print("invalid color")
                color_input = input("green, yellow, red, blue, or white\n").lower()
            h.give_hint(None, color_input)
        elif type_input.lower() == "v":
            value_input = int(input("A number 1 - 5\n"))
            while value_input > 5 or value_input < 0:
                print("invalid number")
                value_input = int(input("A number 1 - 5\n"))
            h.give_hint(value_input, None)
    else:
        print("Invalid action\n")
        continue
    h.change_player()
