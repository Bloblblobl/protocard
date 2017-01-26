import os
from datetime import datetime


class Message(object):
    def __init__(self, text, player_id, game_state=None, mtype='message', timestamp=None):
        self.timestamp = timestamp if timestamp else datetime.now()
        self.player_id = player_id
        self.text = text
        self.game_state = game_state
        self.mtype = mtype

    def display_message(self, day_date=False, hour=True, minute=True, second=True):
        player_id = 'GOD' if self.player_id == 0 else f'Player {self.player_id}'
        return '[{}] {}: {}'.format(self.get_timestamp(day_date, hour, minute, second), player_id, self.text)
    
    def get_timestamp(self, day_date=False, hour=True, minute=True, second=True):
        timestamp = ''
        if day_date:
            timestamp += '{}/{}/{}'.format(str(self.timestamp.month).zfill(2),
                                           str(self.timestamp.day).zfill(2),
                                           str(self.timestamp.year).zfill(2))
            if hour or minute or second:
                timestamp += '|'
        if hour:
            timestamp += str(self.timestamp.hour).zfill(2)
            if minute or second:
                timestamp += ':'
        if minute:
            timestamp += str(self.timestamp.minute).zfill(2)
            if second:
                timestamp += ':'
        if second:
            timestamp += str(self.timestamp.second).zfill(2)
        return timestamp

    def get_message(self):
        return Message(self.text, self.player_id, self.game_state, self.mtype, self.timestamp)


class MessageLog(object):
    def __init__(self, name, messages=[]):
        self.messages = []
        self.name = name

        for message in messages:
            self.messages.append(message)

    def add_message(self, text, player_id, game_state=None, mtype='message', timestamp=None):
        if player_id == 'curr':
            player_id = game_state.curr_player.player_id
        new_message = Message(text, player_id, game_state, mtype, timestamp)
        self.messages.append(new_message)

    def add_messages(self, messages):
        for m in messages:
            self.add_message(m.text, m.player_id, m.game_state, m.mtype, m.timestamp)

    def get_log(self, log_pos=0, display_len=0, excluded_types=['hidden'], start_time=None, end_time=None):
        if log_pos == 'all':
            return self.messages

        # Apply filters
        message_list = []
        for message in self.messages:
            if excluded_types:
                if message.mtype in excluded_types:
                    continue

            if start_time:
                if message.timestamp < start_time:
                    continue
            if end_time:
                if message.timestamp > end_time:
                    continue

            message_list.append(message)

        # Correct default display length
        display_len = len(message_list) if display_len == 0 else display_len

        # Return a subsection of the message log
        return message_list[log_pos:(log_pos + display_len)]

    def get_game_state(self, timestamp):
        try:
            return self.messages[timestamp].game_state
        except KeyError:
            self.add_message('Message does not exist', 0, mtype='error')

    def write_to_file(self, log_pos=0, display_len=0, excluded_types=['hidden'], start_time=None, end_time=None):
        if not os.path.isidr('logfiles'):
            os.makedirs('logfiles')
        f = open(f'logfiles/{self.name}.txt', 'w+')
        message_list = self.get_log(log_pos, display_len, excluded_types, start_time, end_time)
        for message in message_list:
            f.write(message.display_message() + '\n')

    def sort_log(self, filters=[]):
        try:
            self.messages.sort(key=lambda x: tuple(getattr(x, f) for f in filters))
        except AttributeError:
            self.messages.sort()

