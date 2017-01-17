try:
    from protocard.card import Card
except ImportError:
    from card import Card


class Zone(object):
    def __init__(self, ztype, deck_name=None, cards=None, max_size=7):
        self.ztype = ztype
        self.cards = cards if cards else []
        self.max_size = max_size

        if deck_name:
            self.parse_file(deck_name)

    def __repr__(self):
        return "<{} cards:{} max size:{}>".format(
            self.ztype, len(self.cards), self.max_size)

    def parse_file(self, file_path):
        # MOVE TO EXTERNAL TOOL
        for line in open(file_path, 'r'):
            card = line.split('|')
            self.cards.append(Card(card[0], card[1], card[2], card[3]))
