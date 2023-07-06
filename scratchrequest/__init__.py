from ._session import *
from ._twcloud import *

def Login(username : str, password : str):
  return Session.login(username=username, password=password)
