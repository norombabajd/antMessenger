from Profile import Message, Profile
from ds_messenger import DirectMessenger, DirectMessengerError
import time

sender = Profile()
sender_online = DirectMessenger()
sender.username = 'johndanieln'
sender.password = 'zotzot9148'
sender.dsuserver = '168.235.86.101'
sender_online.username = 'johndanieln'
sender_online.password = 'zotzot9148'
sender_online.dsuserver = '168.235.86.101'
sender.save_profile("/Users/johndaniel/Desktop/johndaniel.dsu")

reciever = Profile()
reciever_online = DirectMessenger()
reciever.username = 'maybejohndaniel'
reciever.password = 'zotzot9148'
reciever.dsuserver = '168.235.86.101'
reciever_online.username = 'maybejohndaniel'
reciever_online.password = 'zotzot9148'
reciever_online.dsuserver = '168.235.86.101'
reciever.save_profile("/Users/johndaniel/Desktop/notjohndaniel.dsu")


# SEND AND STORE TO MAYBEJOHNDANIEL
test_msg = Message('maybejohndaniel', 'hey finsta!')
sender.store_sent(test_msg)
sender_online.send(test_msg.entry, test_msg.recipient)


second_msg = Message('johndanieln', 'hey main!')
reciever.store_sent(second_msg)
reciever_online.send(test_msg.entry, test_msg.recipient)


    john = sender_online.retrieve_new()
    sender.store_recieved(john)

"""x = 0
while x != 2:
    john = sender_online.retrieve_new()
    sender.store_recieved(john)
    finsta = reciever_online.retrieve_new()
    reciever.store_recieved(finsta)
    x += 1"""

sender.save_profile("/Users/johndaniel/Desktop/johndaniel.dsu")
reciever.save_profile("/Users/johndaniel/Desktop/notjohndaniel.dsu")

[{"entry": "hey main!", "recipient": "johndanieln", "timestamp": "1647224964.288426"}, {"message": "hey finsta!", "from": "johndanieln", "timestamp": "1647224964.20972"}], 

"maybejohndaniel": [{"message": "another go!", "from": "maybejohndaniel", "timestamp": "1647223792.92253"}, {"message": "hey finsta!", "from": "maybejohndaniel", "timestamp": "1647224964.35611"}]}}