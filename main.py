import random
from sys import exit

game_state = {
    'discarded' : [],
    'active' : {},
    'colors' : ['blue', 'green', 'red', 'white', 'yellow'],
    'hints' : 8,
    'fuses' : 3,
    'game_over' : False,
    'current_player' : 0,
    'deck' : [],
    'hand_size' : 5
}

for c in game_state['colors']:
    game_state['active'][c] = []  # List of cards at that index


class Game:
    def __init__(self, players):
        self.last_turn = False
        self.players = players
    # Possible moves during a turn

    def give_hint(self, value, color):  # Pass None for one since only one piece may be given
        if game_state['hints'] > 0:
            game_state['hints'] -= 1

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
        if game_state['hints'] < 8 and card_index in range(5):
            game_state['hints'] += 1
            game_state['discarded'].append(player.hand.pop(card_index))
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

        if card_index in range(game_state['hand_size']):

            # if the card being played is one greater than the last card on that pile,
            # AND they're the same color, we play it
            if game_state['active'][pile][-1].value is (player.hand[card_index].value - 1) and pile is player.hand[card_index].color:
                game_state['active'][pile].append(player.hand.pop(card_index))
                player.cards_known.pop(card_index)
                game_state['active'][pile].append(player.hand[card_index])

            else:
                game_state['fuses'] -= 1
                cur_fuses = 3 - game_state['fuses']
                print("Play invalid: either value or color does not follow\nIgniting fuse number " + str(cur_fuses) + "...")

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
            return True

        else:
            print("Game should have already ended")
            return False

    def is_over(self):

        answer = False

        if game_state['fuses'] is 0:
            game_state['game_over'] = True
            answer = True

        if len(_deck) is 0:
            answer = True

        if len(sum(game_state['active'].values(), [])) == len(game_state['colors']) * 5:
            game_state['game_over'] = True
            answer = True

        # Calculate final score if the game is over
        if answer:
            score_sum = 0
            for color in game_state['colors']:
                score_sum += max(game_state['active'][color])
            print("GAME OVER\nFinal score is " + str(score_sum))

        return answer

    def change_player(self):
        game_state['current_player'] = ((game_state['current_player'] + 1) % len(self.players))

    def other_player_number(self):
        return (game_state['current_player'] + 1) % len(self.players)


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return self.color + " - " + str(self.value)


class Player:
    def __init__(self, number):
        self.hand = []
        self.cards_known = []
        self.number = number
        game_state['hand_size'] = 5
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
        for _ in range(game_state['hand_size']):
            self.hand.append(_deck.pop())


class AIPlayer(Player):
    # NEVER LET THE AI SEE THEIR OWN HAND

    def __init__(self, number):
        super().__init__(number)
        self.actions = ['p', 'h', 'd']

    def ai_decide_initial_action(self, game):

        decision = -1

        if game_state['hints'] is 0:
            self.ai_decide_action_discard_card(game)

        return None

    def ai_decide_action_play_card(self, game):
        return 0,

    def ai_decide_action_give_hint(self, game):
        return None

    def ai_decide_action_discard_card(self, game):

        return None


def create_deck():
    deck_length = 50
    deck = []
    for color in game_state['colors']:
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


# Game Loop
_deck = create_deck()  # already shuffled
h = Game([AIPlayer(0), AIPlayer(1)])

while not game_state['game_over']:
    initial_action = h.players[game_state['current_player']].ai_decide_initial_action(h)
    if initial_action == "p":
        print("AI Player " + str(game_state['current_player']) + " playing a card")
        _card_num, _pile = h.players[game_state['current_player']].ai_decide_action_play_card(h)
        if not h.play(h.players[game_state['current_player']], _card_num, _pile):
            print("Player failed to play card!")
            exit()
    elif initial_action == "d":
        print("AI Player " + str(game_state['current_player']) + " playing a card")
        _card_num = h.players[game_state['current_player']].ai_decide_action_discard_card(h)
        if not h.discard(h.players[game_state['current_player']], _card_num):
            print("Player failed to discard card!")
            exit()
    elif initial_action == "h":
        print("AI Player " + str(game_state['current_player']) + " giving a hint")
        _value, _color = h.players[game_state['current_player']].ai_decide_action_give_hint(h)
        if not h.give_hint(_value, _color):
            print("Player failed to give hint!")
            exit()

    # Handles print statements
    if h.is_over():
        break
