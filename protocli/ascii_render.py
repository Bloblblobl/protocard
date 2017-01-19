from math import floor


def fit_info(text, length, alignment='left', spc=' '):
    if len(str(text)) < length:
        sp_len = (length - len(str(text)))

        def left():
            return str(text) + spc * sp_len

        def right():
            return spc * sp_len + str(text)

        def mid():
            l = (floor(sp_len / 2))
            r = (sp_len - l)
            return l * spc + str(text) + r * spc

        options = {'left': left,
                   'right': right,
                   'mid': mid}
        return options[alignment]()
    else:
        return str(text)[0:length]


def _extend_map(r_map, size):
    for i in range(0, size):
        r_map.append('')
    return r_map


def _render_empty_hand_card(r_map, sp):
    r_map[sp + 0] += '   ▄▄▄▄▄▄▄▄▄▄▄   '
    r_map[sp + 1] += '   █         █   '
    r_map[sp + 2] += '   █         █   '
    r_map[sp + 3] += '   █         █   '
    r_map[sp + 4] += '   █    ╳    █   '
    r_map[sp + 5] += '   █         █   '
    r_map[sp + 6] += '   █         █   '
    r_map[sp + 7] += '   █         █   '
    r_map[sp + 8] += '   ▀▀▀▀▀▀▀▀▀▀▀   '


def render_enemy_hand(hand, r_map, sp=0):
    # sp - starting point for the render map
    r_map = _extend_map(r_map, 9)
    for i in range(0, hand.max_size):
        if i < len(hand.cards):
            r_map[sp + 0] += '   ▄▄▄▄▄▄▄▄▄▄▄   '
            r_map[sp + 1] += '   █▓▓▓▓▓▓▓▓▓█   '
            r_map[sp + 2] += '   █▓▓▓▓▓▓▓▓▓█   '
            r_map[sp + 3] += '   █▓▓▓▓▓▓▓▓▓█   '
            r_map[sp + 4] += '   █▓▓▓▓▓▓▓▓▓█   '
            r_map[sp + 5] += '   █▓▓▓▓▓▓▓▓▓█   '
            r_map[sp + 6] += '   █▓▓▓▓▓▓▓▓▓█   '
            r_map[sp + 7] += '   █▓▓▓▓▓▓▓▓▓█   '
            r_map[sp + 8] += '   ▀▀▀▀▀▀▀▀▀▀▀   '
        else:
            _render_empty_hand_card(r_map, sp)
    _add_border_to_lines(r_map, sp, 8)
    return sp + 9


def render_player_hand(hand, r_map, sp=0):
    # sp - starting point for the render map
    r_map = _extend_map(r_map, 9)
    for i in range(0, hand.max_size):
        if i < len(hand.cards):
            card = hand.cards[i]
            num = fit_info(i, 2, 'right', '#')
            c = 'CC'
            name = fit_info(card.name, 9, 'mid')
            effects = '.....'
            atk = fit_info(card.attack_stat, 2, spc='/')
            hlt = fit_info(card.health_stat, 2, 'right', '\\')

            r_map[sp + 0] += '   ▄▄▄▄▄▄▄▄▄▄▄   '
            r_map[sp + 1] += '   █##│   │CC█   '.replace('##', num).replace('CC', c)
            r_map[sp + 2] += '   █──╯   ╰──█   '
            r_map[sp + 3] += '   █~~NAME!~~█   '.replace('~~NAME!~~', name)
            r_map[sp + 4] += '   █  .....  █   '.replace('.....', effects)
            r_map[sp + 5] += '   █         █   '
            r_map[sp + 6] += '   █──╮   ╭──█   '
            r_map[sp + 7] += '   █AA│   │HH█   '.replace('AA', atk).replace('HH', hlt)
            r_map[sp + 8] += '   ▀▀▀▀▀▀▀▀▀▀▀   '
        else:
            _render_empty_hand_card(r_map, sp)
    _add_border_to_lines(r_map, sp, 8)
    return sp + 9


def render_board(board, r_map, sp=0):
    # sp - starting point for the render map
    r_map = _extend_map(r_map, 5)
    for i in range(0, board.max_size):
        if i < len(board.cards):
            card = board.cards[i]
            num = fit_info(i, 3, 'mid', ' ')
            name = fit_info(card.name, 9, 'mid')
            atk = fit_info(card.attack_curr, 2, spc='/')
            hlt = fit_info(card.health_curr, 2, 'right', '\\')

            if card.exhausted:
                r_map[sp + 0] += '   ╭┄┄┄┄┄┄┄┄┄╮   '
                r_map[sp + 1] += '   ┆  NAME!  ┆   '.replace('~~NAME!~~', name)
                r_map[sp + 2] += '   ├┄┄╮   ╭┄┄┤   '
                r_map[sp + 3] += '   ┆AA┆###┆HH┆   '.replace('AA', atk).replace('HH', hlt).replace('###', num)
                r_map[sp + 4] += '   ╰┄┄┴┄┄┄┴┄┄╯   '
            else:
                r_map[sp + 0] += '   ╭─────────╮   '
                r_map[sp + 1] += '   │~~NAME!~~│   '.replace('~~NAME!~~', name)
                r_map[sp + 2] += '   ├──╮   ╭──┤   '
                r_map[sp + 3] += '   │AA│###│HH│   '.replace('AA', atk).replace('HH', hlt).replace('###', num)
                r_map[sp + 4] += '   ╰──┴───┴──╯   '
        else:
            r_map[sp + 0] += '   ╭─────────╮   '
            r_map[sp + 1] += '   │         │   '
            r_map[sp + 2] += '   │    ╳    │   '
            r_map[sp + 3] += '   │         │   '
            r_map[sp + 4] += '   ╰─────────╯   '

    _add_border_to_lines(r_map, sp, 4)
    return sp + 5


def render_border_top(r_map, sp):
    r_map = _extend_map(r_map, 1)
    r_map[sp] = '╔' + '═' * 119 + '╗'
    return sp + 1


def render_border_bottom(r_map, sp):
    r_map = _extend_map(r_map, 1)
    r_map[sp] = '╚' + '═' * 119 + '╝'
    return sp + 1


def render_border_divider(r_map, sp):
    r_map = _extend_map(r_map, 1)
    r_map[sp] = '╠' + '═' * 119 + '╣'
    return sp + 1


def render_splitter(r_map, sp, game_state, player=False):
    r_map = _extend_map(r_map, 3)
    if player:
        player_health = game_state.other_player.player_health
    else:
        player_health = game_state.curr_player.player_health
    r_map[sp + 0] = '╠' + '═' * 23 + '╗' + ' ' * 78 + '╔' + '═' * 16 + '╣'
    r_map[sp + 1] = '║ ▼ ENEMY BATTLEFIELD ▼ ╠' + '═' * 38 + str(player_health) + '═' * 38 + '╣ ▲ ENEMY HAND ▲ ║'
    r_map[sp + 2] = '╠' + '═' * 23 + '╝' + ' ' * 78 + '╚' + '═' * 16 + '╣'

    if player:
        r_map[sp + 1] = r_map[sp + 1].replace('ENEMY', ' YOUR').replace('▼', '~').replace('▲', '▼').replace('~', '▲')

    return sp + 3


def _add_border_to_lines(r_map, sp, num, extenders=[]):
    for i in range(sp, sp + num + 1):
        if i in extenders:
            r_map[i] = '║' + r_map[i] + '╠'
        else:
            r_map[i] = '║' + r_map[i] + '║'


def add_empty_line(r_map, sp):
    r_map = _extend_map(r_map, 1)
    r_map[sp] = '║' + ' ' * 119 + '║'
    return sp + 1
