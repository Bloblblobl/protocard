class GameState(object):
    def __init__(self, players):
        self.players = {}
        for i in range(0, len(players)):
            self.players[players[i].player_id] = players[i]
        self.curr_player = self.players[1]
        self.other_player = self.players[2]

        self.action_log = []
        self.game_log = []
