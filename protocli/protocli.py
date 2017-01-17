import os

try:
    from protocard.protocli.ascii_render import render_enemy_hand, render_board, render_player_hand
except ImportError:
    from protocli.ascii_render import render_enemy_hand, render_board, render_player_hand
try:
    from protocard.player import Player
except ImportError:
    from player import Player
try:
    from protocard.card import Card
except ImportError:
    from card import Card
try:
    from protocard.game_controller import GameController
except ImportError:
    from game_controller import GameController


def welcome_message():
    os.system('cls')
    message_file = open('protocli/welcome_screen.txt', 'r')
    message = ''
    for line in message_file:
        message += line
    print(message)
    input()
    os.system('cls')


def render_map(game_state):
    os.system('cls')
    r_map = []
    sp = 0
    enemy = game_state.other_player
    player = game_state.curr_player

    sp = render_enemy_hand(enemy.hand, r_map, sp)
    sp = render_board(enemy.board, r_map, sp)
    sp = render_board(player.board, r_map, sp)
    render_player_hand(player.hand, r_map, sp)
    for line in r_map:
        print(line)
    for action in game_state.action_log:
        print(action)


def main():
    players = [Player(1, 'tests/deck1.txt'), Player(2, 'tests/deck2.txt')]
    gc = GameController(players)
    welcome_message()
    game_state = gc.start_game()
    while True:
        render_map(game_state)
        game_state = gc.manage_turn()


if __name__ == '__main__':
    main()
