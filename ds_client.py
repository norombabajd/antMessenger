# John Daniel Norombaba
# jnoromba@uci.edu
# 91483000

# Audrey Nguyen
# audrehn3@uci.edu
# 50253773

# ds_client.py
# Contains the send() function, communicates with DSU servers.

import socket
from types import NoneType
import ds_protocol

def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  
  # Initalize.
  change_bio = False
  
  # Test for invalid parameter types, check for bio management.
  if (type(message) in [str, None, NoneType]) and (type(bio) in [str, None, NoneType]):
    change_bio = True if type(bio) is str else change_bio  # Check for bio-changes.
    # Check for whitespace in bio.
    if (type(bio) is str and len(bio.split()) == 0):
      return False
    # Check for whitespace in message if bio not present
    if (type(message) is str) and (len(message.split()) == 0) and (type(bio) in [None, NoneType]):
      return False
    # Check for whitespace (not empty string) in message if bio is present.
    if (message == '') and (type(bio) is str) and (len(bio.split()) != 0):
      pass
    elif (type(message) is str) and (len(message.split()) == 0) and (type(bio) is str) and (len(bio.split()) != 0):
      return False
  else:
    # Illegal types are being passed into message or bio (not str or None).
    return False

  try:
    # Create the client, with a default time-out value of 3 seconds.
    socket.setdefaulttimeout(3)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Establish a connection to the DSU server.
    client.connect((server, port))
  except socket.error or socket.timeout:
    # If the socket fails to connect to the server.  
    return False
  except Exception:
    # Assume all other cases are errors.
    client.close()
    return False

  try:
    # Connect to the server, and create a response 
    client.send(ds_protocol.join(username, password))
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