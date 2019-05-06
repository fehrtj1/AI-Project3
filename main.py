import random


class Game:
    def __init__(self, clues, players):

        self.discarded_cards = []
        self.active_cards = {}

        self.time_tokens = 8
        self.fuse_tokens = 3
        self.game_lost = False
        self.clues = clues
        self.players = players
        self.current_player = players[0].number

    ### Possible moves during a turn

    def give_hint(self, card_indices, value, color): # Pass None for one since only one piece may be given
        if self.time_tokens > 0:
            self.time_tokens -= 1

            if value is None and color is not None or value is not None and color is None:
                for i in card_indices:
                    if value is None:
                        self.players[self.other_player_number()].cards_known[i].color = color
                    if color is None:
                        self.players[self.other_player_number()].cards_known[i].value = value

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

    def initial_draw(self, deck):
        for _ in range(5):
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


# Game Loop
_deck = create_deck()  # already shuffled
hanabi = Game([], [Player(0), Player(1)])

while not hanabi.game_lost:
    pass
