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
    r_map = _extend_map(r_map, 10)
    for i in range(0, hand.max_size):
        try:
            r_map[sp + 0] += '   ▄▄▄▄▄▄▄▄▄▄▄   '
            r_map[sp + 1] += '   █▓▓▓▓▓▓▓▓▓█   '
            r_map[sp + 2] += '   █▓▓▓▓▓▓▓▓▓█   '
            r_map[sp + 3] += '   █▓▓▓▓▓▓▓▓▓█   '
            r_map[sp + 4] += '   █▓▓▓▓▓▓▓▓▓█   '
            r_map[sp + 5] += '   █▓▓▓▓▓▓▓▓▓█   '
            r_map[sp + 6] += '   █▓▓▓▓▓▓▓▓▓█   '
            r_map[sp + 7] += '   █▓▓▓▓▓▓▓▓▓█   '
            r_map[sp + 8] += '   ▀▀▀▀▀▀▀▀▀▀▀   '
        except:
            _render_empty_hand_card(r_map, sp)
    r_map[sp + 9] = ''
    return sp + 10


def render_player_hand(hand, r_map, sp=0):
    # sp - starting point for the render map
    r_map = _extend_map(r_map, 10)
    for i in range(0, hand.max_size):
        try:
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
        except Exception as e:
            _render_empty_hand_card(r_map, sp)
    r_map[sp + 9] = ''
    return sp + 10


def render_board(board, r_map, sp=0):
    # sp - starting point for the render map
    r_map = _extend_map(r_map, 6)
    for i in range(0, board.max_size):
        try:
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
        except Exception as e:
            r_map[sp + 0] += '   ╭─────────╮   '
            r_map[sp + 1] += '   │         │   '
            r_map[sp + 2] += '   │    ╳    │   '
            r_map[sp + 3] += '   │         │   '
            r_map[sp + 4] += '   ╰─────────╯   '

    r_map[sp + 5] = ''
    return sp + 6
