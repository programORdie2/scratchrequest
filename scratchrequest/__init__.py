from ._session import *
from ._twcloud import *
from ._project import *

def Login(username : str, password : str):
  return Session.login(username=username, password=password)

def get_project(id: int):
  return CreateConnectProject(id=id)
