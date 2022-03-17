# Audrey Nguyen
# audrehn3@uci.edu
# 50253773
#
# John Daniel Norombaba
# jnoromba@uci.edu
# 91483000
#
# test_ds_messenger.py
# Tests send(), retrieve_new(), and retrieve_all functions from ds_messenger.py.
#
# ICS 32 Winter 2022
# Final Exam: Chatting with Friends

from ds_messenger import DirectMessenger

assert(DirectMessenger.send('Hello World!', 'aud') == True)
assert((DirectMessenger.send(1, 'aud') == False))

assert(DirectMessenger.retrieve_new() == ['{"entry": "Hello World!","recipient":"aud", "timestamp": "1603167689.3928561"}'])

DirectMessenger.send('Second message' 'aud')
assert(DirectMessenger.retrieve_all() == ['{"entry": "Hello World!","recipient":"aud", "timestamp": "1603167689.3928561"}', '{"entry": "Second message","recipient":"aud", "timestamp": "1603167689.3928561"}'])