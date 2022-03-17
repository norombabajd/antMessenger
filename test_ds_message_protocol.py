# John Daniel Norombaba
# jnoromba@uci.edu
# 91483000

# Audrey Nguyen
# audrehn3@uci.edu
# 50253773

# test_ds_message_protocol.py
# Tests all(), new(), and send() methods from ds_messenger.py.

from ds_message_protocol import send, all, new, extract_json

tokens = ["450e2846-3ae1-418a-8aa6-f6ea586b7e0c", "hLBcnWQFkVNXOCVhoVInh574xwMD+rfxCPIpNOgUPw4=", "N9vhv41IqIz1vTEFEsI1pnHwsDvtFYRYIfK7MLYFVXw=", ""]
entries = ['{"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}', '{"entry": "Hey!","recipient":"notjohndaniel", "timestamp": "2603420689.2928565"}', '{"entry": "yooo!","recipient":"aud", "timestamp": "2603420689.2928565"}', {}]


def construct_send():
  """"""
  global tokens
  global entries

  try:
    assert send(tokens[0], entries[0]).decode('utf-8') == '{"token":"450e2846-3ae1-418a-8aa6-f6ea586b7e0c", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}'
    assert send(tokens[1], entries[1]).decode('utf-8') == '{"token":"hLBcnWQFkVNXOCVhoVInh574xwMD+rfxCPIpNOgUPw4=", "directmessage": {"entry": "Hey!","recipient":"notjohndaniel", "timestamp": "2603420689.2928565"}}'
    assert send(tokens[2], entries[2]).decode('utf-8') == '{"token":"N9vhv41IqIz1vTEFEsI1pnHwsDvtFYRYIfK7MLYFVXw=", "directmessage": {"entry": "yooo!","recipient":"aud", "timestamp": "2603420689.2928565"}}'
  except Exception as ex:
    print("construct_send() : construction : tests failed (not-intended).\n", ex)
  else:
    print("construct_send() : construction : tests passed (as-intended).")
  
  try:
    assert send(tokens[3], entries[3]).decode('utf-8') == {"token":"", "directmessage": {}}
  except Exception as ex:
    print("construct_send() : no token : failed (as-intended).\n")
  else:
    print("construct_send() : no token : tests passed (not-intended).")
  

def construct_new():
  try:
    assert new(tokens[0]).decode('utf-8') == '{"token":"450e2846-3ae1-418a-8aa6-f6ea586b7e0c", "directmessage": "new"}'
    assert new(tokens[1]).decode('utf-8') == '{"token":"hLBcnWQFkVNXOCVhoVInh574xwMD+rfxCPIpNOgUPw4=", "directmessage": "new"}'
    assert new(tokens[2]).decode('utf-8') == '{"token":"N9vhv41IqIz1vTEFEsI1pnHwsDvtFYRYIfK7MLYFVXw=", "directmessage": "new"}'
  except Exception as ex:
    print("construct_new()  : construction : tests failed (not-intended).\n", ex)
  else:
    print("construct_new()  : construction : tests passed (as-intended).")
  
  try:
    assert new(tokens[3]).decode('utf-8') == '{"token":"", "directmessage": ""}'
  except Exception as ex:
    print("construct_new()  : no token : tests failed (as-intended).\n", ex)
  else:
    print("construct_new()  : no token : tests passed (not-intended).")
  
  
def construct_all():
  try:
    assert new(tokens[0]).decode('utf-8') == '{"token":"450e2846-3ae1-418a-8aa6-f6ea586b7e0c", "directmessage": "all"}'
    assert new(tokens[1]).decode('utf-8') == '{"token":"hLBcnWQFkVNXOCVhoVInh574xwMD+rfxCPIpNOgUPw4=", "directmessage": "all"}'
    assert new(tokens[2]).decode('utf-8') == '{"token":"N9vhv41IqIz1vTEFEsI1pnHwsDvtFYRYIfK7MLYFVXw=", "directmessage": "all"}'
  except Exception as ex:
    print("construct_all()  : construction : tests failed (not-intended).\n", ex)
  else:
    print("construct_all()  : construction : tests passed (as-intended).")
  
  try:
    assert new(tokens[3]).decode('utf-8') == '{"token":"", "directmessage": "all"}'
  except Exception as ex:
    print("construct_all()  : no token : tests failed (as-intended).\n", ex)
  else:
    print("construct_all()  : no token : tests passed (not-intended).")


    


if __name__ == "__main__":
  # construct_send()
  construct_new()
  construct_all()