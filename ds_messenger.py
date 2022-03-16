# John Daniel Norombaba
# jnoromba@uci.edu
# 91483000
#
# Audrey Nguyen
# audrehn3@uci.edu
# 50253773
#
# ds_messenger.py
# Handles sending and receiving messages and DirectMessenger class.

import socket, time
import ds_protocol
from ds_protocol import DSProtocolError

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None

class DirectMessengerError(Exception):
  """Encapsulates socket and json related errors."""
  pass

class DirectMessenger:
  """Enables peer to peer communication over a compatible dsuserver."""
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token:str = None
    self.dsuserver:str = dsuserver
    """Instantiates the object's default DSU server."""
    self.username:str = username
    """Instantiates the object's default username."""
    self.password:str = password
    """Instantiates the object's default password."""
	
  def _communicate(self, protocol:bytes):
    """Communicates with a dsuserver, sending each function's respective protocol."""
    try:
      # Establish a connection over the internet and send.
      socket.setdefaulttimeout(3)
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client.connect((self.dsuserver, 3021))
      client.send(protocol)
      # Return the server's response.
      return ds_protocol.extract_json(client.recv(4096))
    except socket.error or socket.timeout:
      # Handle communication errors with socket.
      raise DirectMessengerError("There was a problem communicating with the DSU Server.")
    except TypeError:
      # Handle client.connect() attempting to connect to a NoneType IP address.
      raise DirectMessengerError("Your profile does not contain a dsuserver to connect to.")
    except DSProtocolError:
      raise DirectMessengerError("There was a problem interpreting the data retrieved.")

  def _validate(self, protocol:str, data:tuple):
    """Ensures data returned from server follows dsuserver protocol."""
    try:
      if protocol in data.response and data.type == 'ok':
        # Check for specific data in a response (ex: 'messages', 'token').
        return data
      elif protocol == 'send' and data.type == 'ok':
        # Check for an 'ok' after sending a message.
        return data
      else:
        # If data is mismatched.
        raise DirectMessengerError("The data returned from the server cannot be interpreted.")
    except:
      # If returned data does not follow protocol.
      raise DirectMessengerError("The data returned from the server cannot be interpreted.")
  
  def _login(self):
    """ Retrieves user token if none is present. """
    if self.token != None:
      return
    try:
      data = self._communicate(ds_protocol.join(self.username, self.password))
      self._validate('token', data)
      self.token = data.response['token']
    except DirectMessengerError as dme:
      print(dme)
    except DSProtocolError as dpe:
      print(dpe)

  def send(self, message:str, recipient:str) -> bool:
    """INSERT DESCRIPTION HERE."""
    try:
      self._login()
      entry = f'{{"entry": "{message}", "recipient": "{recipient}", "timestamp": {time.time()}}}'
      response = self._communicate(ds_protocol.send(self.token, entry))
      self._validate('send', response)
      return True
    except DirectMessengerError as dme:
      print(dme)
      return False
    except DSProtocolError as dpe:
      print(dpe)
      return False

  def retrieve_new(self) -> list:
    """INSERT DESCRIPTION HERE."""
    try:
      self._login()
      data = self._communicate(ds_protocol.new(self.token))
      self._validate('messages', data)
      return data.messages
    except DirectMessengerError as dme:
      print(dme)
    except DSProtocolError as dpe:
      print(dpe)

  def retrieve_all(self) -> list:
    """INSERT DESCRIPTION HERE."""
    try:
      self._login()
      data = self._communicate(ds_protocol.all(self.token))
      self._validate('messages', data)
      return data.messages
    except DirectMessengerError as dme:
      print(dme)
    except DSProtocolError as dpe:
      print(dpe)