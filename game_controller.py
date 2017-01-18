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

        elif command.startswith('atk'):
            command = command[3:]
            command_pieces = command.split(',')
            if len(command_pieces) != 2:
                print('Attack what???')
                return False
            try:
                self.manage_attack(int(command_pieces[0]), int(command_pieces[1]))
                return self.game_state
            except ValueError:
                print('Attack what???')
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
        self._check_for_deaths(player.player_id)

    def manage_attack(self, attack_num, defend_num):
        try:
            attacker = self.game_state.curr_player.board.cards[attack_num]
            defender = self.game_state.other_player.board.cards[defend_num]
        except IndexError:
            self.game_state.action_log.append('Invalid Target(s)')
            return

        self.game_state.curr_player.attack(attacker, defender)
        self.game_state.action_log.append('Player {} Attacked Player {}\'s {} with {}'.format(
            self.game_state.curr_player.player_id,
            self.game_state.other_player.player_id,
            defender.name,
            attacker.name
        ))

        self._check_for_deaths(1)
        self._check_for_deaths(2)

    def _check_for_deaths(self, player_id):
        dead_cards = self.game_state.players[player_id].check_for_deaths()
        for card in dead_cards:
            self.game_state.action_log.append('Player {} lost their {}'.format(player_id, card.name))

    def pass_turn(self):
        # Switch players
        old_curr_player = self.game_state.curr_player
        self.game_state.curr_player = self.game_state.other_player
        self.game_state.other_player = old_curr_player

        # Refresh action log and store last turn in game log
        for item in self.game_state.action_log:
            self.game_state.game_log.append(item)
        self.game_state.action_log = []

        # Draw one at the beginning of the turn if there's room
        if len(self.game_state.curr_player.hand.cards) < self.game_state.curr_player.hand.max_size:
            self.manage_draw(self.game_state.curr_player, 1)
        return self.game_state

    def manage_turn(self):
        result = False
        while not result:
            command = input('>>>')
            result = self.manage_command(command)

        return result
