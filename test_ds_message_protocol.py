# John Daniel Norombaba
# jnoromba@uci.edu
# 91483000

# Audrey Nguyen
# audrehn3@uci.edu
# 50253773

# test_ds_message_protocol.py
# Tests all(), new(), and send() methods from ds_messenger.py.

from ds_protocol import send, all, new

token = ""
entries = ""


user_token = "450e2846-3ae1-418a-8aa6-f6ea586b7e0c"
entry = {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}

def construct_send():
    pass


"""def send(user_token:str, entry:str):
  try:
    if user_token != None and len(entry.split()) != 0:
      return encode_json(f'{{"token": "{user_token}", "directmessage": {entry}}}')
    else:
      raise DSProtocolError("Invalid entry or token type provided.")
  except AttributeError or TypeError:
    raise DSProtocolError("Invalid bio or token type provided.") 

def new(user_token):
  try:
    if user_token != None:
      return encode_json(f'{{"token":"{user_token}", "directmessage": "new"}}')
    else:
      raise DSProtocolError("No token provided.")
  except AttributeError or TypeError:
    raise DSProtocolError("Invalid token type provided.") 

def all(user_token):
  try:
    if user_token != None:
      return encode_json(f'{{"token":"{user_token}", "directmessage": "all"}}')
    else:
      raise DSProtocolError("No token provided.")
  except AttributeError or TypeError:
    raise DSProtocolError("Invalid token type provided.") 
"""
    


def assert_all():
    global user_token
    try:
        assert all(user_token).decode('utf-8') == '{"token":"450e2846-3ae1-418a-8aa6-f6ea586b7e0c", "directmessage": "all"}'
        assert all('').decode('utf-8') == '{"token":"", "directmessage": "all"}'
    except AssertionError as ae:
        print(ae)
    print("assert_all() performed.")

def assert_new():
    global user_token
    try:
        assert new(user_token).decode('utf-8') == {"token":"450e2846-3ae1-418a-8aa6-f6ea586b7e0c", "directmessage": "new"}
        assert new('').decode('utf-8') == {"token":"", "directmessage": "new"}
    except AssertionError as ae:
        print(ae)
    print("assert_new() performed.")

def assert_send():
    global user_token
    global entry
    try:
        assert send(user_token, entry).decode('utf-8') == {"token":"450e2846-3ae1-418a-8aa6-f6ea586b7e0c", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}
        assert(send('', {}).decode('utf-8')) == {"token":"", "directmessage": {}}
    except AssertionError as ae:
        print(ae)
    print("assert_send() performed.")

def test(func1, func2, func3):
    func1()    
    func2()   
    func3()

if __name__ == "__main__":
    test(assert_all, assert_new, assert_send)
