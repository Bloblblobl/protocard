try:
    from protocard.Card import Card
except Exception as e:
    from Card import Card


class Zone(object):
    def __init__(self, ztype, deck_name=None, cards=None, max_size=7):
        self.ztype = ztype
        self.cards = cards if cards else []
        self.max_size = max_size

        if deck_name:
            self.parse_file(deck_name)

    def __repr__(self):
        return "<Deck player:{} cards:{}>".format(
            self.player, len(self.cards))

    def parse_file(self, file_path):
        for line in open(file_path, 'r'):
            card = line.split('|')
            self.cards.append(Card(card[0], card[1], card[2], card[3]))

    def render_cards(self, start=0, length=0):
        if length == 0:
            for card in self.cards:
                card.standalone_render()
        else:
            for i in range(start, length):
                try:
                    self.cards[i].standalone_render()
                except Exception as e:
                    print(e)
