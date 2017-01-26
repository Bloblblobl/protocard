import os
import sys

from math import ceil

try:
    from protocard.game_state import GameState
except ImportError:
    from game_state import GameState


class GameController(object):
    def __init__(self, players):
        self.game_state = GameState(players)

    def start_game(self):
        self.manage_draw(self.game_state.curr_player, 7, 'hidden')
        self.manage_draw(self.game_state.other_player, 7, 'hidden')
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
            player_logs = self.game_state.curr_player.action_log.get_log(excluded_types=[]) + \
                          self.game_state.other_player.action_log.get_log(excluded_types=[])
            self.game_state.game_log.add_messages(player_logs)
            self.game_state.game_log.sort_log(['timestamp', 'player_id'])

            self.game_state.game_log.write_to_file(excluded_types=[])
            for player in self.game_state.players.values():
                player.action_log.write_to_file()
            os.system('cls')
            sys.exit()

        print('That\'s not even a command!!!')
        return False

    def manage_draw(self, player, num, mtype='message'):
        result = player.draw_cards(num)
        if type(result) == str:
            self.game_state.curr_player.action_log.add_message(result, player.player_id, self.game_state, 'error')
        else:
            for card in result:
                self.game_state.curr_player.action_log.add_message(f'Drew {card.info_message()}',
                                                                   player.player_id,
                                                                   self.game_state,
                                                                   mtype)

    def manage_play_card(self, player, hand_pos, mtype='message'):
        result = player.play_card(hand_pos)
        if type(result) == str:
            self.game_state.curr_player.action_log.add_message(result, player.player_id, self.game_state, 'error')
        else:
            self.game_state.curr_player.action_log.add_message(f'Played {result.info_message()}',
                                                               player.player_id,
                                                               self.game_state,
                                                               mtype)
        self._check_for_deaths(player.player_id)

    def manage_attack(self, attack_num, defend_num):
        try:
            attacker = self.game_state.curr_player.board.cards[attack_num]
            defender = self.game_state.other_player.board.cards[defend_num]
        except IndexError:
            self.game_state.curr_player.action_log.add_message('Invalid Target(s)', 'curr', self.game_state, 'error')
            return

        self.game_state.curr_player.attack(attacker, defender)
        self.game_state.curr_player.action_log.add_message(f'{attacker.name} attacked {defender.name}',
                                                           'curr',
                                                           self.game_state)

        self._check_for_deaths(1)
        self._check_for_deaths(2)

    def _check_for_deaths(self, player_id):
        dead_cards = self.game_state.players[player_id].check_for_deaths()
        for card in dead_cards:
            self.game_state.curr_player.action_log.add_message(f'{card.name} died', player_id, self.game_state)

    def pass_turn(self):
        # Switch players
        old_curr_player = self.game_state.curr_player
        self.game_state.curr_player = self.game_state.other_player
        self.game_state.other_player = old_curr_player
        self.game_state.curr_turn += 1

        turn_num = ceil(self.game_state.curr_turn / 2)
        self.game_state.curr_player.action_log.add_message(f'Turn {turn_num} Begins', 'curr', self.game_state)
        self.game_state.new_turn = True

        # Draw one at the beginning of the turn if there's room
        if len(self.game_state.curr_player.hand.cards) < self.game_state.curr_player.hand.max_size:
            self.manage_draw(self.game_state.curr_player, 1)
        return self.game_state

    def manage_turn(self):
        self.game_state.new_turn = False
        result = False
        while not result:
            command = input('>>>')
            result = self.manage_command(command)

        return result
