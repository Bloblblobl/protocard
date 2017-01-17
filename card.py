class Card(object):
    def __init__(self, name, descr, attack, health):
        self.name = name
        self.descr = descr
        self.attack_stat = attack
        self.attack_curr = attack
        self.health_stat = health
        self.health_curr = health
        self.actions = 1
        self.exhausted = False

    def __repr__(self):
        return '<Card name:{} descr:{} attack:{} health:{}>'.format(
            self.name, self.descr, self.attack_curr, self.health_curr)

    def info_message(self):
        return '{}: {}/{}'.format(self.name, self.attack_stat, self.health_stat)

    def on_play(self):
        pass
