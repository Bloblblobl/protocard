import os

try:
    from protocard.protocli import ascii_render
except ImportError:
    from protocli import ascii_render
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


def display_message(message_path, replacer=None, replacee=None):
    os.system('cls')
    message_file = open(message_path, 'r', encoding="utf8")
    message = ''
    for line in message_file:
        if replacer and replacee:
            for i in range(len(replacer)):
                line = line.replace(replacer[i], replacee[i])
        message += line
    print(message)
    input()
    os.system('cls')


def render_whole_board(game_state):
    enemy = game_state.other_player
    player = game_state.curr_player
    r_map = []
    sp = 0

    # A little messy right now, will be cleaned up
    sp = ascii_render.render_border_top(r_map, sp)
    sp = ascii_render.add_empty_line(r_map, sp)
    sp = ascii_render.render_enemy_hand(enemy.hand, r_map, sp)
    sp = ascii_render.add_empty_line(r_map, sp)
    sp = ascii_render.render_splitter(r_map, sp, game_state)
    sp = ascii_render.add_empty_line(r_map, sp)
    sp = ascii_render.render_board(enemy.board, r_map, sp)
    sp = ascii_render.add_empty_line(r_map, sp)
    sp = ascii_render.render_border_divider(r_map, sp)
    sp = ascii_render.add_empty_line(r_map, sp)
    sp = ascii_render.render_board(player.board, r_map, sp)
    sp = ascii_render.add_empty_line(r_map, sp)
    sp = ascii_render.render_splitter(r_map, sp, game_state, True)
    sp = ascii_render.add_empty_line(r_map, sp)
    sp = ascii_render.render_player_hand(player.hand, r_map, sp)
    sp = ascii_render.add_empty_line(r_map, sp)
    ascii_render.render_border_bottom(r_map, sp)

    # Add action log to render map
    r_map[3] += ' ACTION LOG:'
    for i in range(0, len(game_state.action_log)):
        try:
            r_map[i + 4] += ' ' + game_state.action_log[i]
        except IndexError:
            continue

    for line in r_map:
        print(line)


def render_map(game_state):
    os.system('cls')
    if game_state.new_turn:
        if game_state.curr_player.player_id == 2:
            display_message('protocli/display/new_turn.txt', ['@','✡'], ['2','†'])
        else:
            display_message('protocli/display/new_turn.txt', ['@'], ['1'])
    render_whole_board(game_state)


def main():
    players = [Player(1, 'tests/deck1.txt'), Player(2, 'tests/deck2.txt')]
    gc = GameController(players)
    display_message('protocli/display/welcome_screen.txt')
    game_state = gc.start_game()
    while True:
        render_map(game_state)
        game_state = gc.manage_turn()


if __name__ == '__main__':
    main()
