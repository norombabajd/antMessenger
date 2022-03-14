# Audrey Nguyen
# audrehn3@uci.edu
# 50253773
#
# John Daniel Norombaba
# jnoromba@uci.edu
# 91483000
#
# Profile.py
# Adapted from Mark S. Baldwin's Profile.py
#
# ICS 32 Winter 2022
# Final Exam: Chatting with Friends


import json, time, os
from pathlib import Path


"""
DsuFileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to load or save Profile objects to file the system.

"""
class DsuFileError(Exception):
    pass

"""
DsuProfileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to deserialize a dsu file to a Profile object.

"""
class DsuProfileError(Exception):
    pass


class Message(dict):
    """ 

    The Post class is responsible for working with individual user posts. It currently supports two features: 
    A timestamp property that is set upon instantiation and when the entry object is set and an 
    entry property that stores the post message.

    """
    def __init__(self, recipient:str = None, entry:str = None, timestamp:float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)
        self.set_recipient(recipient)
        dict.__init__(self, entry=self._entry, recipient=self._recipient, timestamp=self._timestamp)
    
    def set_entry(self, entry):
        self._entry = entry 
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = str(time.time())

    def set_recipient(self, recipient):
        self._recipient = recipient
        dict.__setitem__(self, 'recipient', recipient)

    def get_entry(self):
        return self._entry
    
    def set_time(self, time:float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    
    def get_time(self):
        return self._timestamp

    def get_recipient(self):
        return self._recipient

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)
    recipient = property(get_recipient, set_recipient)
    
    
class Profile:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver # REQUIRED
        self.username = username # REQUIRED
        self.password = password # REQUIRED
        self.bio = ''            # OPTIONAL
        self._conversations = {}         # OPTIONAL
    
    def store_sent(self, message: Message) -> None:
        if message.recipient not in self._conversations:
            self._conversations[message.recipient] = []
        self._conversations[message.recipient].append(message)

    def store_recieved(self, messages:list[dict]):
        for msg in messages:
            if msg['from'] not in self._conversations:
                self._conversations[msg['from']] = []
            self._conversations[msg['from']].append(msg)

    def get_conversation(self) -> dict[Message]:
        return self._conversations

    def dispose_conversation(self, recipient:str) -> None:
        if recipient in self._conversations:
            del self._conversations[recipient]

    def save_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("An error occurred while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                
                for user in obj['_conversations']:
                    self._conversations[user] = []
                    for convo in obj['_conversations'][user]:
                        if 'recipient' in convo:
                            msg = Message(convo['recipient'], convo['entry'], convo['timestamp'])
                            self._conversations[user].append(msg)
                        elif 'from' in convo:
                            self._conversations[user].append(msg)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()