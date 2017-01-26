try:
    from protocard.message_log import MessageLog
except ImportError:
    from message_log import MessageLog


class GameState(object):
    def __init__(self, players):
        self.players = {}
        for i in range(0, len(players)):
            self.players[players[i].player_id] = players[i]
        self.curr_player = self.players[1]
        self.other_player = self.players[2]

        self.game_log = MessageLog(f'gamelog')
        self.new_turn = False
        self.curr_turn = 1
