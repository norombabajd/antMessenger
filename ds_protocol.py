# John Daniel Norombaba
# jnoromba@uci.edu
# 91483000

# Audrey Nguyen
# audrehn3@uci.edu
# 50253773

# ds_protocol.py
# Handles protocols that communicate with the DSU server.

import json, time
from collections import namedtuple

class DSProtocolError(Exception):
  pass

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['response','type', 'messages'])

def join(username:str, password:str) -> str:
  """ Constructs and encodes the join protocol. """
  try:
    # Test for whitespace and encode.
    if username.split() != 0 and password.split() != 0:
      return encode_json(f'{{"join": {{"username": "{username}","password": "{password}","token":""}}}}')
    else:
      raise DSProtocolError("No username or password given.")
  except AttributeError or TypeError:
    raise DSProtocolError("Invalid username or password provided.")
  
def post(user_token:str, message:str) -> str:
  """ Constructs and encodes the post protocol. """
  try:
    # Test for whitespace and encode.
    if len(message.split()) != 0:
      return encode_json(f'{{"token": "{user_token}", "post": {{"entry": "{message}", "timestamp": {time.time()}}}}}')
    else:
      raise DSProtocolError("No message provided.")
  except AttributeError or TypeError:
    # Tests for unsupported types or issues when calling split.
    raise DSProtocolError("Invalid message or token type provided.")

def update_bio(user_token:str, bio:str) -> str:
  """ Constructs and encodes the bio protocol. """
  try:
    if len(bio.split()) != 0:
      msg = f'{{"token": "{user_token}", "bio": {{"entry": "{bio}", "timestamp": "1603167689.3928561"}}}}'
      return encode_json(msg)
  except AttributeError or TypeError:
    raise DSProtocolError("Invalid bio or token type provided.")

def send(user_token:str, entry:str):
  """ Send a directmessage to another DS user. """
  try:
    if user_token != None and len(entry.split()) != 0:
      return encode_json(f'{{"token": "{user_token}", "directmessage": {entry}}}')
    else:
      raise DSProtocolError("Invalid entry or token type provided.")
  except AttributeError or TypeError:
    raise DSProtocolError("Invalid bio or token type provided.") 

def new(user_token):
  """ Request unread message from the DS server. """
  try:
    if user_token != None:
      return encode_json(f'{{"token":"{user_token}", "directmessage": "new"}}')
    else:
      raise DSProtocolError("No token provided.")
  except AttributeError or TypeError:
    raise DSProtocolError("Invalid token type provided.") 

def all(user_token):
  """ Request all messages from DS server. """
  try:
    if user_token != None:
      return encode_json(f'{{"token":"{user_token}", "directmessage": "all"}}')
    else:
      raise DSProtocolError("No token provided.")
  except AttributeError or TypeError:
    raise DSProtocolError("Invalid token type provided.") 

def extract_json(json_msg:json) -> DataTuple:
  '''
  Converts json objects into a Python namedtuple.
  :param json_msg: A message encoded in json.

  '''
  try:
    messages = []
    json_obj = json.loads(json_msg)    
    response = json_obj['response']
    type = json_obj['response']['type']
    if 'messages' in response:
        messages = response['messages']

  except json.JSONDecodeError as e:
    print("ERROR: JSON response cannot be decoded.")
    return DataTuple(response={'type': 'error'}, type='error', messages=None)
  except:
    print("ERROR: Response cannot be decoded.")
    return DataTuple(response={'type': 'error'}, type='error', messages=None)

  return DataTuple(response, type, messages)

def encode_json(str_msg:str) -> str:
  '''
  Encodes objects into json, utf-8.
  :param str_msg: A string message/bio type.
  
  '''
  return str_msg.encode('utf-8')