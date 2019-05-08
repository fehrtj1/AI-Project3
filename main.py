import random
from sys import exit

game_state = {
    'discarded': [],
    'active': {},
    'colors': ['blue', 'green', 'red', 'white', 'yellow'],
    'hints': 8,
    'fuses': 3,
    'game_over': False,
    'current_player': 0,
    'deck': [],
    'hand_size': 5
}

for c in game_state['colors']:
    game_state['active'][c] = []  # List of cards at that index


def flatten(l):
    return [item for sublist in l for item in sublist]


class Game:
    def __init__(self, players):

        self.last_turn = False
        self.players = players
        self.max_playable = 25
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

    # We can specialize our decisions based on how far along we are in the game
    def is_early(self):
        return 25 >= 25 - self.get_active_card_count() >= 17

    def is_mid(self):
        return 16 >= 25 - self.get_active_card_count() >= 10

    def is_late(self):
        return 9 >= 25 - self.get_active_card_count() >= 0

    # Returns how many cards are in the piles
    def get_active_card_count(self):
        return len(flatten(game_state['active'].values()))

    # Returns the number of cards needed of a given value in the current active cards across all piles
    def n_value_needed(self, v):

        if v < 1 or v > 5:
            print("Value Error: Card value does not exist.")
            return None

        # For example, if we need a 4, that means there are 3's on top of a pile, so we subtract 1
        # None signifies we need a 1 in that spot. i.e. No cards have been played yet there
        v = None if v is 1 else (v - 1)

        n = 0

        for color in game_state['colors']:
            n = n + (1 if game_state['active'][color][-1].value is v else 0)
        return n


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return self.color + " - " + str(self.value)

    def __eq__(self, other):
        return self.color is other.color and self.value is other.value and self.value is not None and self.color is not None


class Player:
    def __init__(self, number):
        self.hand = []
        self.cards_known = []
        self.number = number
        self.initial_draw()

    def num_cards(self, color, value):
        if color is not None and value is not None:
            count = 0
            for card in self.hand:
                if card == Card(color, value):
                    count += 1
            return count
        if color is None and value is not None:
            count = 0
            for card in self.hand:
                if card.value == value:
                    count += 1
            return count
        if color is not None and value is None:
            count = 0
            for card in self.hand:
                if card.color is color:
                    count += 1
            return count
        return -1

    def num_known_cards(self, color, value):
        if color is not None and value is not None:
            count = 0
            for card in self.cards_known:
                if card == Card(color, value):
                    count += 1
            return count
        if color is None and value is not None:
            count = 0
            for card in self.cards_known:
                if card.value == value:
                    count += 1
            return count
        if color is not None and value is None:
            count = 0
            for card in self.cards_known:
                if card.color is color:
                    count += 1
            return count
        return -1

    def print_hand(self):
        i = 0
        for card in self.cards_known:
            print("Card at index " + str(i) + ": " +
                  card.color if card.color is not None else "Unknown color - " + str(card.value) if card.value is not None else "Unknown value")
            i += 1

    def print_full_hand(self):
        for card in self.hand:
            print(card + "\n")

    # Draw 5 at the start of the game
    def initial_draw(self):
        for _ in range(game_state['hand_size']):
            self.hand.append(_deck.pop())
            self.cards_known.append(Card(None, None))


class AIPlayer(Player):
    # NEVER LET THE AI SEE THEIR OWN HAND

    def __init__(self, number):
        super().__init__(number)
        self.actions = ['p', 'h', 'd']

    def ai_decide_initial_action(self, game):

        potential_play = self.get_playable_card()
        decision = -1

        if game_state['hints'] >= 1 and not self.is_cards_known_complete():
            decision = 1

        # If we have no hint tokens and we have no plays, we are practically forced to discard
        # Improvements would take into account late game and fuse count to guess a likely (say, 50% + 15%*fuse count)
        # This makes it more careful the closer we are to losing by igniting all the fuses. For example, It will not
        # Guess here if there is only one fuse remaining unless it is 90% certain that it would be a successful play
        if game_state['hints'] is 0 and potential_play is None:
            decision = 2

        # Play if we have full information on a valid card. This is always the optimal play
        if potential_play is not None:
            decision = 0

        if decision is -1:
            # if we can't do anything else, do our safest option, which is discarding
            decision = 2

        return self.actions[decision]

    def ai_decide_action_play_card(self, game):
        play = self.get_playable_card()
        index_of_play = self.hand.index(play)
        return index_of_play, play.color

    def ai_decide_action_give_hint(self, game):
        random.seed()
        # Randomly pick if we should give a color hint or a value hint
        if random.random() > 0.6:
            # Give color hint
            rand_color = game_state['colors'][random.randint(0, len(game_state['colors']))]
            while game.players[game.other_player_number()].num_cards(rand_color, None) <= 0 < game.players[game.other_player_number()].num_known_cards(rand_color, None):
                rand_color = game_state['colors'][random.randint(0, len(game_state['colors']))]
            return None, rand_color
        else:
            weighted_list = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
            rand_value = weighted_list[random.randint(0, 10)]
            while game.players[game.other_player_number()].num_cards(None, rand_value) <= 0 < game.players[game.other_player_number()].num_known_cards(None, rand_value):
                rand_value = weighted_list[random.randint(0, 10)]
            return rand_value, None
            # Give value hint


    def ai_decide_action_discard_card(self, game):

        index_to_discard = self.hand.index(self.get_first_useless())

        if index_to_discard is not None:
            return index_to_discard

        else:
            return random.randint(0, 4)

    def have_playable_card(self):
        for card in self.cards_known:

            # If we have full info on a card
            if card.color is not None and card.value is not None:
                for color in game_state['colors']:

                    # and if that card has a valid position to play on
                    if game_state['active'][color][-1].value + 1 is card.value and game_state['active'][color][-1].color is card.color:

                        # return it to play on
                        return card

        # Also need to perform process of elimination to see if a card appears that way as well, but this project scope creeped us so hard
        return None

    def is_cards_known_complete(self):
        sum = 0
        for card in self.cards_known:
            if card.color is not None and card.value is not None:
                sum += 1

        return True if sum is game_state['hand_size'] else False

    def get_first_useless(self):
        for card in self.cards_known:
            if card.color is not None and card.value is not None and card in self.get_used_list():
                # Just get the first one since that's all we can operate on,
                # and because we will run this check again next turn
                return card
        return None


    def get_used_list(self):
        used = []
        for card in game_state['discarded']:
            used.append(card)

        for color in game_state['colors']:
            for card in game_state['active'][color]:
                used.append(card)
        return used

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
        print("AI Player " + str(game_state['current_player']) + " playing a card\n")
        _card_num, _pile = h.players[game_state['current_player']].ai_decide_action_play_card(h)
        if not h.play(h.players[game_state['current_player']], _card_num, _pile):
            print("Player failed to play card!")
            exit()
    elif initial_action == "d":
        print("AI Player " + str(game_state['current_player']) + " discarding a card\n")
        _card_num = h.players[game_state['current_player']].ai_decide_action_discard_card(h)
        if not h.discard(h.players[game_state['current_player']], _card_num):
            print("Player failed to discard card!")
            exit()
    elif initial_action == "h":
        print("AI Player " + str(game_state['current_player']) + " giving a hint\n")
        _value, _color = h.players[game_state['current_player']].ai_decide_action_give_hint(h)
        print("Hint was " + (str(_value) if _value is not None else _color) + "\n")
        if not h.give_hint(_value, _color):
            print("Player failed to give hint!")
            exit()

    # Handles print statements for which loss event occurred
    if h.is_over():
        break
