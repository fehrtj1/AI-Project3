import random
from sys import exit

colors = ['blue', 'green', 'red', 'white', 'yellow']

game_state = {

}


def flatten(l):
    return [item for sublist in l for item in sublist]


class Game:
    def __init__(self, players):
        self.discarded_cards = []
        self.active_cards = {}
        for color in colors:
            self.active_cards[color] = []  # List of cards at that index

        self.time_tokens = 8
        self.fuse_tokens = 3
        self.game_over = False
        self.players = players
        self.current_player = players[0].number  # always start with player 0
        self.last_turn = False

    # Possible moves during a turn

    def give_hint(self, value, color):  # Pass None for one since only one piece may be given
        if self.time_tokens > 0:
            self.time_tokens -= 1

            if value is None and color is not None or value is not None and color is None:
                if value is None:
                    self.add_information(color, None, self.players[self.other_player_number()])
                if color is None:
                    self.add_information(None, value, self.players[self.other_player_number()])
            else:
                print("Too much or not enough hint information")
            self.change_player()
            return True
        else:
            print("No tokens available to give hint")
            return False

    @staticmethod
    def add_information(color, value, player):
        for i in range(len(player.cards_known)):
            if color is not None and player.hand[i].color == color:
                player.cards_known[i].color = color
            if value is not None and player.hand[i].value == value:
                player.cards_known[i].value = value

    def discard(self, player, card_index):
        if self.time_tokens < 8 and card_index in range(5):
            self.time_tokens += 1
            self.discarded_cards.append(player.hand.pop(card_index))
            player.cards_known.pop(card_index)
            player.draw(player, _deck)
            self.change_player()
            return True
        else:
            print("Either no tokens or not a valid")
            return False

    # player = one playing the card
    # card_index = which card in player hand
    # pile = where to play that card, is a color
    def play(self, player, card_index, pile):

        if card_index in range(5):

            # if the card being played is one greater than the last card on that pile,
            # AND they're the same color, we play it
            if self.active_cards[pile][-1].value is (player.hand[card_index].value - 1)\
                    and pile is player.hand[card_index].color:
                self.active_cards[pile].append(player.hand.pop(card_index))
                player.cards_known.pop(card_index)
                self.active_cards[pile].append(player.hand[card_index])
                if len(sum(self.active_cards.values(), [])) == len(colors) * 5:
                    self.game_over = True
                    print("Game win")
                    return True
            else:
                self.fuse_tokens -= 1
                cur_fuses = 3 - self.fuse_tokens
                print(R"Play invalid: either value or color does not follow"
                      R"Igniting fuse number " + str(cur_fuses) + "...")
                if cur_fuses is 0:
                    self.game_over = True
                    print("All fuses have been lit, game is over")

            self.change_player()
            return True
        else:
            print("card not in player's hand")
            return False

    def draw(self, player):

        if len(_deck) >= 1:
            new_card = _deck.pop()
            player.hand[player.hand.index(None)] = new_card
            player.cards_known.append(Card(None, None))
            if len(_deck) is 0:
                print("One turn remaining, draw pile empty")
                self.last_turn = True
            return True
        else:
            print("Game should have already ended")
            return False

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

    def __eq__(self, other):
        return self.color is other.color and self.value is other.value


class Player:
    def __init__(self, number):
        self.hand = []
        self.cards_known = []
        self.number = number
        self.hand_size = 5
        self.initial_draw()

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
            self.hand.append(_deck.pop())


class AIPlayer(Player):
    # NEVER LET THE AI SEE THEIR OWN HAND

    def ai_decide_initial_action(self, game):
        return None

    def ai_decide_action_play_card(self, game):
        return None, None

    def ai_decide_action_give_hint(self, game):
        return None, None

    def ai_decide_action_discard_card(self, game):
        return None


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
h = Game([AIPlayer(0), AIPlayer(1)])


while not h.game_over:
    initial_action = h.players[h.current_player].ai_decide_initial_action(h)
    if initial_action == "p":
        print("AI Player " + h.current_player + " playing a card")
        _card_num, _pile = h.players[h.current_player].ai_decide_action_play_card(h)
        if not h.play(h.players[h.current_player], _card_num, _pile):
            print("Player failed to play card!")
            exit()
    elif initial_action == "d":
        print("AI Player " + h.current_player + " playing a card")
        _card_num = h.players[h.current_player].ai_decide_action_discard_card(h)
        if not h.discard(h.players[h.current_player], _card_num):
            print("Player failed to discard card!")
            exit()
    elif initial_action == "h":
        print("AI Player " + h.current_player + " giving a hint")
        _value, _color = h.players[h.current_player].ai_decide_action_give_hint(h)
        if not h.give_hint(_value, _color):
            print("Player failed to give hint!")
            exit()
