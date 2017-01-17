import os
import sys

try:
    from protocard.game_state import GameState
except ImportError:
    from game_state import GameState


class GameController(object):
    def __init__(self, players):
        self.game_state = GameState(players)

    def start_game(self):
        self.manage_draw(self.game_state.curr_player, 7, True)
        self.manage_draw(self.game_state.other_player, 7, True)
        return self.game_state

    def manage_command(self, command):
        if command.startswith('draw'):
            try:
                self.manage_draw(self.game_state.curr_player, int(command[4:]))
                return self.game_state
            except ValueError:
                print('Draw how much???')
                return False
        elif command.startswith('play'):
            try:
                self.manage_play_card(self.game_state.curr_player, int(command[4:]))
                return self.game_state
            except ValueError:
                print('Play what???')
                return False
        elif command.startswith('pass'):
            return self.pass_turn()
        elif command == 'exit':
            os.system('cls')
            sys.exit()
        print('That\'s not even a command!!!')
        return False

    def manage_draw(self, player, num, hidden=False):
        result = player.draw_cards(num)
        if not hidden:
            if type(result) == str:
                self.game_state.action_log.append(result)
            else:
                for card in result:
                    self.game_state.action_log.append('Player {} Drew {}'.format(player.player_id, card.info_message()))

    def manage_play_card(self, player, hand_pos, hidden=False):
        result = player.play_card(hand_pos)
        if not hidden:
            if type(result) == str:
                self.game_state.action_log.append(result)
            else:
                self.game_state.action_log.append('Player {} Played {}'.format(player.player_id, result.info_message()))

    def pass_turn(self):
        # Switch players
        old_curr_player = self.game_state.curr_player
        self.game_state.curr_player = self.game_state.other_player
        self.game_state.other_player = old_curr_player

        # Draw one at the beginning of the turn
        self.manage_draw(self.game_state.curr_player, 1)
        return self.game_state

    def manage_turn(self):
        result = False
        while not result:
            command = input('>>>')
            result = self.manage_command(command)

        return result
