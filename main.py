

class Game:
    def __init__(self, deck, clues):

        self.deck = deck
        self.discarded_cards = []
        self.active_cards = {}

        self.time_tokens = 8
        self.fuse_tokens = 3
        self.game_lost = False
        self.clues = clues

    def turn(self, player, action_number):
        if action_number is 0: # Give one piece of information
            self.time_tokens -= 1

        elif action_number is 1: # Discard a card
            self.time_tokens += 1
            player.draw()
        elif action_number is 2: # Play a card


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



class Clues:
    def __init__(self, colors, values, relevant_player):
        pass


class Player:
    def __init__(self, hand):
        self.hand = hand

    def discard(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return
        print("Card not in hand")

    def draw(self, deck):
        new_card = deck.pop()
        self.hand.append(new_card)

    def get_optimal_card(self):
        pass
