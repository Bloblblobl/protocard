try:
    from protocard.card import Card
except ImportError:
    from card import Card


class Zone(object):
    def __init__(self, ztype: object, deck_name: object = None, cards: object = None, max_size: object = 7) -> object:
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
            try:
                self.cards.append(Card(card[0], card[1], int(card[2]), int(card[3]), card[4], card[5]))
            except IndexError:
                self.cards.append(Card(card[0], card[1], int(card[2]), int(card[3])))