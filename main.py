class Game:
    def __init__(self, deck):

        self.deck = deck
        self.discarded_cards = []
        self.active_cards = {}

        self.time_tokens = 8
        self.fuse_tokens = 3
        self.game_lost = False

    def turn(self, player, action_number):
        if action_number is 0: # Give one piece of information
        elif action_number is 1: # Discard a card
        elif action_number is 2: # Play a card
        else:
            print("Not a valid action")

    def discard(self, player, card):
        player.discard(card)

    def play(self, player, card):

        if card in player.hand:
            if self.active_cards[card.color][-1] is (card.value + 1)
                self.active_cards[card.color].extend(card.value)
            else:
                self.fuse_tokens -= 1
                cur_fuses = 3 - self.fuse_tokens
                print("Play invalid, igniting fuse number " + str(3 - self.fuse_tokens))
                if cur_fuses is 0:
                    self.game_lost = True





class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

class Clues:
    def __init__(self, colors, values):

class Player:
    def __init__(self, hand, clues):
        self.hand = hand
        self.clues = clues

    def discard(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return
        print("Card not in hand")

    def draw(self, deck):
        new_card = deck.pop()
        self.hand.append(new_card)

    def play(self, card):
        if card in hand:

        else:
            print("card not in players hand")

class AI_Player(Player):
    def __init__(self, hand, clues):
        super().__init__(hand, clues)

