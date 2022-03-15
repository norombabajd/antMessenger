from Profile import Message, Profile
from ds_messenger import DirectMessenger, DirectMessengerError
import time

sender = Profile()
sender_online = DirectMessenger()
sender.username = 'notjohndaniel'
sender.password = 'zotzot9148'
sender.dsuserver = '168.235.86.101'
sender_online.username = 'notjohndaniel'
sender_online.password = 'zotzot9148'
sender_online.dsuserver = '168.235.86.101'
sender.save_profile("/Users/johndaniel/Desktop/notjohndaniel.dsu")

reciever = Profile()
reciever_online = DirectMessenger()
reciever.username = 'maybejohndaniel'
reciever.password = 'zotzot9148'
reciever.dsuserver = '168.235.86.101'
reciever_online.username = 'maybejohndaniel'
reciever_online.password = 'zotzot9148'
reciever_online.dsuserver = '168.235.86.101'
reciever.save_profile("/Users/johndaniel/Desktop/maybejohndaniel.dsu")



msg1 = Message('maybejohndaniel', 'hey, maybejohndaniel!')
print(msg1)
sender.store_sent(msg1)
sender_online.send(msg1.entry, msg1.recipient)

msg2 = Message('notjohndaniel', 'hey, notjohndaniel!')
print(msg2)
reciever.store_sent(msg2)
reciever_online.send(msg2.entry, msg2.recipient)


inbox1 = sender_online.retrieve_new()
print(inbox1)
sender.store_recieved(inbox1)

inbox2 = reciever_online.retrieve_new()
print(inbox2)
reciever.store_recieved(inbox2)

sender.save_profile("/Users/johndaniel/Desktop/notjohndaniel.dsu")
reciever.save_profile("/Users/johndaniel/Desktop/maybejohndaniel.dsu")