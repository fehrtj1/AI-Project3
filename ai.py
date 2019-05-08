from main import Player, Game, colors


class AIPlayer(Player):
    # NEVER LET THE AI SEE THEIR OWN HAND

    def ai_decide_initial_action(self, game):
        return None

    def ai_decide_action_play_card(self, game):
        return 0,

    def ai_decide_action_give_hint(self, game):
        return None

    def ai_decide_action_discard_card(self, game):
        return None
