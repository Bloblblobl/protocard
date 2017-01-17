try:
    from protocard.zone import Zone
except ImportError:
    from zone import Zone


class Player(object):
    def __init__(self, player_id, deck_name=None):
        self.deck = Zone('Deck', deck_name)
        self.hand = Zone('Hand')
        self.board = Zone('Board')
        self.player_id = player_id

    def draw_cards(self, num):
        drawn_cards = []
        for i in range(0, num):
            if len(self.hand.cards) < self.hand.max_size:
                if self.deck.cards[0]:
                    drawn_cards.append(self.deck.cards[0])
                    del self.deck.cards[0]
                else:
                    return 'Deck is empty'
            else:
                return 'Hand is full'

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
