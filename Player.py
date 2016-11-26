try:
    from protocard.Zone import Zone
except Exception as e:
    from Zone import Zone


class Player(object):
    def __init__(self, id, deck_name=None, max_hand=7, max_board=7):
        self.deck = Zone('Deck', deck_name)
        self.hand = Zone('Hand')
        self.board = Zone('Board')
        self.id = id
        self.max_hand = max_hand
        self.max_board = max_board


    def show_deck(self):
        self.deck.render_cards()
