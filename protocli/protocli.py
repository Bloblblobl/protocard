import os, sys

try:
    from protocard.protocli.ascii_render import render_enemy_hand, \
                                                render_board, \
                                                render_player_hand
except:
    from protocli.ascii_render import render_enemy_hand, \
                                      render_board, \
                                      render_player_hand
try:
    from protocard.Player import Player
except:
    from Player import Player
try:
    from protocard.Card import Card
except:
    from Card import Card


def welcome_message():
    os.system('cls')
    message_file = open('protocli/welcome_screen.txt', 'r')
    message = ''
    for line in message_file:
        message += line
    print(message)
    input()
    os.system('cls')

    num_players = None
    while num_players is None:
        try:
            print('How many players are we working with?')
            num_players = int(input())
        except ValueError:
            os.system('cls')
            print('Sorry, not a valid number! Try again.')
            num_players = None
    os.system('cls')
    return num_players


def generate_players(num_players):
    players = {}
    for i in range(0, num_players):
        try:
            players[i] = Player(i, 'tests/deck{}.txt'.format(i+1))
        except Exception:
            players[i] = Player(i, 'tests/deck1.txt')
    return players


def play_card(player, hand_pos):
    if len(player.board.cards) < player.max_board:
        try:
            player.board.cards.append(player.hand.cards[hand_pos])
            del player.hand.cards[hand_pos]
        except Exception as e:
            print(e)


def handle_command(player):
    command = input('>>> ')
    if command.startswith('p'):
        if command[1:3] == '->':
            play_card(player, int(command[3]))
        return True
    if command == 'exit':
        os.system('cls')
        sys.exit()
    else:

        print('Please try again')
        return False


def play_turn(player, enemy):
    os.system('cls')
    draw_cards(player, 1)
    r_map=[]
    sp = 0
    sp = render_enemy_hand(enemy.hand, r_map, sp)
    sp = render_board(enemy.board, r_map, sp)
    sp = render_board(player.board, r_map, sp)
    sp = render_player_hand(player.hand, r_map, sp)
    for line in r_map:
        print(line)
    command = False
    while not command:
        command = handle_command(player)


def draw_cards(player, num):
    for i in range(0, num):
        if len(player.hand.cards) < player.max_hand:
            try:
                player.hand.cards.append(player.deck.cards[0])
                del player.deck.cards[0]
            except:
                pass


def main():
    num_players = welcome_message()
    players = generate_players(num_players)
    draw_cards(players[0], 7)
    draw_cards(players[1], 7)
    while True:
        play_turn(players[0], players[1])
        play_turn(players[1], players[0])


if __name__ == '__main__':
    main()
