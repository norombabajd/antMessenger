# John Daniel Norombaba
# jnoromba@uci.edu
# 91483000

# Audrey Nguyen
# audrehn3@uci.edu
# 50253773

# ds_messenger.py
# Contains the send() function, communicates with DSU servers.

import socket
from types import NoneType
import ds_protocol


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
		
  def send(self, message:str, recipient:str) -> bool:
    '''
    The send function joins a ds server and sends a message to a recipient

    :param message: The message sent by the user.
    :param recipient: The person receiving the message.
    '''
    
    # Initalize.
    

    try:
      # Create the client, with a default time-out value of 3 seconds.
      socket.setdefaulttimeout(3)
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      # Establish a connection to the DSU server.
      client.connect((server, 3021))
    except socket.error or socket.timeout:
      # If the socket fails to connect to the server.  
      return False
    except Exception:
      # Assume all other cases are errors.
      client.close()
      return False

    try:
      # Connect to the server, and create a response 
      client.send(ds_protocol.join(self.username, self.password))
      server = ds_protocol.extract_json(client.recv(4096))
      # Retrieve user_token by sending the join protocol.
      user_token = server.response['token']
    except socket.error or socket.timeout:
      # If the socket fails to send or recieve a message.
      return False
    except KeyError or ValueError:
      # If the response recieved is not valid: no token.
      client.close()
      return False
    except:
      # Assume all other cases are errors.
      client.close()
      return False

    try: 
      # Continue if the 'join' is successful.
      if server.type == 'ok':
        # Post a message using the post protocol.
        if ds_protocol.post(user_token, message) != "":
          client.send(ds_protocol.post(user_token, message))
          server = ds_protocol.extract_json(client.recv(4096))        
          # Check if message was updated, else return False.
          if server.type != 'ok':
            # Assume non-'ok' responses are errors.
            client.close()
            return False
          else:
            if not change_bio:
              # Return True if message posted, no bio.
              client.close()
              return True
          
        # Update the bio using the bio protocol.
        if type(bio) is not NoneType:
          if ds_protocol.update_bio(user_token, bio) != "":
            client.send(ds_protocol.update_bio(user_token, bio))
            server = ds_protocol.extract_json(client.recv(4096))
            if server.type != 'ok':
              # Assume non-'ok' responses are errors.
              client.close()
              return False
            else:
              client.close()
              return True

    except socket.error or socket.timeout:
      # If the socket fails to send or recieve a message.
      return False
    except KeyError or ValueError as e:
      # If the response does recieved is not valid.
      client.close()
      return False
    except Exception:
      client.close()
      return False
		
  def retrieve_new(self) -> list:
    # returns a list of DirectMessage objects containing all new messages
    pass
 
  def retrieve_all(self) -> list:
    # returns a list of DirectMessage objects containing all messages
    pass