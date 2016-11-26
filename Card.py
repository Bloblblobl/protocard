class Card(object):
    def __init__(self, name, descr, attack, health):
        self.name = name
        self.descr = descr
        self.attack = attack
        self.health = health
        self.actions = 1
        self.exhausted = False

    def __repr__(self):
        return "<Card name:{} descr:{} attack:{} health:{}>".format(
            self.name, self.descr, self.attack, self.health)

    def on_play(self):
        pass
