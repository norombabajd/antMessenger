# Audrey Nguyen
# audrehn3@uci.edu
# 50253773
#
# John Daniel Norombaba
# jnoromba@uci.edu
# 91483000
#
# ds_message_protocol.py
# Creates sendable data for and processes data from a DSU server.
#
# ICS 32 Winter 2022
# Final Exam: Chatting with Friends

import json, time
from collections import namedtuple

class DSProtocolError(Exception):
  """DSProtocolError is raised when there was an issue constructing a protocol or handling data from a DSU server."""
  pass

DataTuple: namedtuple = namedtuple('DataTuple', ['response','type', 'messages'])
"""DataTuple is a namedtuple that will store responses from a DSU server."""


def send(user_token:str, entry:str):
  """Send a directmessage to another DS user."""
  try:
    if user_token != None and len(entry.split()) != 0:
      return encode_json(f'{{"token":"{user_token}", "directmessage": {entry}}}')
    else:
      raise DSProtocolError("Invalid entry or token type provided.")
  except AttributeError or TypeError:
    raise DSProtocolError("Invalid bio or token type provided.") 

def new(user_token):
  """Request unread message from the DS server."""
  try:
    if user_token != None:
      return encode_json(f'{{"token":"{user_token}", "directmessage": "new"}}')
    else:
      raise DSProtocolError("No token provided.")
  except AttributeError or TypeError:
    raise DSProtocolError("Invalid token type provided.") 

def all(user_token):
  """Request all messages from DS server."""
  try:
    if user_token != None:
      return encode_json(f'{{"token":"{user_token}", "directmessage": "all"}}')
    else:
      raise DSProtocolError("No token provided.")
  except AttributeError or TypeError:
    raise DSProtocolError("Invalid token type provided.") 

def extract_json(json_msg:json) -> DataTuple:
  """Accepts and decodes a JSON object to DataTuple."""
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
  """Accepts and encodes a string object to JSON, UTF-8."""
  return str_msg.encode('utf-8')