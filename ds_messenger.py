# John Daniel Norombaba
# jnoromba@uci.edu
# 91483000

# Audrey Nguyen
# audrehn3@uci.edu
# 50253773

# ds_messenger.py
# Contains the send() function, communicates with DSU servers.
import time
import socket
from types import NoneType
import ds_protocol
from Profile import Post


class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None

class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
    self.dsuserver = dsuserver
    self.username = username
    self.password = password
	
  def get_token(self):
    """
    Function to join server and get the token if successful.
    """
    # Create the client, with a default time-out value of 3 seconds.
    try:
      socket.setdefaulttimeout(3)
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client.connect(("168.235.86.101", 3021))
      client.send(ds_protocol.join(self.username, self.password))
      server = ds_protocol.extract_json(client.recv(4096))
      # Retrieve user_token by sending the join protocol.
      self.token = server.response['token']
      return True
    except socket.error or socket.timeout:
      # If the socket fails to connect to the server.  
      return False
    except KeyError or ValueError:
      # Assume all other cases are errors.
      client.close()
      return False

  def send(self, message:str, recipient:str) -> bool:
    self.get_token() if self.token == None else None
    # {"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}
    # entry = {"entry": message,"recipient":recipient, "timestamp": "1603167689.3928561"}
    # returns true if message successfully sent, false if send failed.
    p = Post()
    timestamp = p.get_time()
    entry = f'{{"token":"450e2846-3ae1-418a-8aa6-f6ea586b7e0c", "directmessage": {{"entry": "Hello!","recipient":"aud", "timestamp": {timestamp}}}}}'
    try:
      socket.setdefaulttimeout(3)
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client.connect(("168.235.86.101", 3021))
      client.send(entry.encode('utf-8'))
      server = ds_protocol.extract_json(client.recv(4096))
      if server.type == 'ok':
        return True
      else:
        return False
    except socket.error or socket.timeout:
      # If the socket fails to connect to the server.  
      return False
    except KeyError or ValueError:
      # Assume all other cases are errors.
      client.close()
      return False
		
  def retrieve_new(self) -> list:
    self.get_token() if self.token == None else None
    # returns a list of DirectMessage objects containing all new messages
    try:
      socket.setdefaulttimeout(3)
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client.connect(("168.235.86.101", 3021))
      client.send(ds_protocol.new(self.token))
      server = ds_protocol.extract_json(client.recv(4096))
      return server.response['message']
    except socket.error or socket.timeout:
      # If the socket fails to connect to the server.  
      return False
    except KeyError or ValueError:
      # Assume all other cases are errors.
      client.close()
      return False
 
  def retrieve_all(self) -> list:
    self.get_token() if self.token == None else None
    # returns a list of DirectMessage objects containing all messages
    try:
      socket.setdefaulttimeout(3)
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client.connect(("168.235.86.101", 3021))
      client.send(ds_protocol.new(self.token))
      server = ds_protocol.extract_json(client.recv(4096))
      return server.response['messages']
    except socket.error or socket.timeout:
    # If the socket fails to connect to the server.  
      return False
    except KeyError or ValueError:
    # Assume all other cases are errors.
      client.close()

  
  
if __name__ == "__main__":
  d = DirectMessenger()
  d2 = DirectMessenger()

  d.username = "johndanieln"
  d.password = "zotzot9148"
  
  d2.username = "aud"
  d2.password = "aud1234"
  
  for i in range(5):
    d.send("Hello2!", "aud")

  d2.retrieve_all()