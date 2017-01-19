try:
    from protocard.zone import Zone
except ImportError:
    from zone import Zone


class Player(object):
    def __init__(self, player_id, deck_name=None, health = 30):
        self.deck = Zone('Deck', deck_name)
        self.hand = Zone('Hand')
        self.board = Zone('Board')
        self.graveyard = Zone('Graveyard')
        self.player_id = player_id
        self.player_health = health

    def draw_cards(self, num):
        drawn_cards = []
        if num > self.hand.max_size - len(self.hand.cards):
            return 'No room in hand'

        for i in range(0, num):
            if self.deck.cards[0]:
                drawn_cards.append(self.deck.cards[0])
                del self.deck.cards[0]
            else:
                return 'Deck is empty'

        for card in drawn_cards:
            self.hand.cards.append(card)
        return drawn_cards

    def play_card(self, hand_pos):
        try:
            played_card = self.hand.cards[hand_pos]
            if len(self.board.cards) < self.board.max_size:
                if played_card:
                    self.board.cards.append(played_card)
                    del self.hand.cards[hand_pos]
                else:
                    return 'Card is not in hand'
            else:
                return 'Board is full'
        except IndexError:
            return 'Card is not in hand'

        return played_card

    def attack(self, attacker, defender):
        defender.take_damage(attacker.attack_curr)
        if hasattr(defender, 'attack_stat'):
            attacker.take_damage(defender.attack_curr)

    def take_damage(self, damage):
        new_health = self.player_health - damage
        self.player_health = 0 if new_health <= 0 else new_health

    def check_for_deaths(self):
        dead_cards = []
        for i in range(0, len(self.board.cards)):
            try:
                if self.board.cards[i].health_curr == 0:
                    self.graveyard.cards.append(self.board.cards[i])
                    dead_cards.append(self.board.cards[i])
                    del self.board.cards[i]
            except IndexError:
                continue

        return dead_cards
