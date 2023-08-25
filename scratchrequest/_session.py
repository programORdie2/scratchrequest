from ._exceptions import LoginError
from . import _cloud
from . import _project
from . import _settings
import requests, json, re

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36", "x-csrftoken": "a", "x-requested-with": "XMLHttpRequest", "referer": "https://scratch.mit.edu"}

class Session:
    def __init__(self, username: str, session_id: str):
        self.session_id = session_id
        self.username = username
        self.headers = headers
        self._login()

    def _login(self):
        self.cookies = {"scratchcsrftoken" : "a", "scratchlanguage" : "en", "scratchpolicyseen": "true", "scratchsessionsid" : self.session_id, "accept": "application/json", "Content-Type": "application/json"}
        account = requests.post("https://scratch.mit.edu/session", headers=self.headers, cookies={"scratchsessionsid": self.session_id, "scratchcsrftoken": "a", "scratchlanguage": "en"}).json()
        try:
            self.xtoken = account["user"]["token"]
            self.headers["X-Token"] = self.xtoken
            self.all_login_data = account
            self.id = account['user']['id']
            self.username = account['user']['username']
            self.banned = account['user']['banned']
            self.email = account['user']['email']
            self.new_scratcher = account['permissions']['new_scratcher']
            self.get_csrf_token()
        except KeyError:
            raise LoginError("Your login data was wrong. Check if you spelled your credits correctly, or if you are in replit, see the docs for more information.")

    def get_csrf_token(self):
        headers = {"x-requested-with": "XMLHttpRequest", "Cookie": "scratchlanguage=en;permissions=%7B%7D;", "referer": "https://scratch.mit.edu"}
        request = requests.get("https://scratch.mit.edu/csrf_token/", headers=headers)
        self.csrf_token = re.search("scratchcsrftoken=(.*?);", request.headers["Set-Cookie"]).group(1)
        
    def _login_pass(username: str, password: str):
        try:
            response = requests.post("https://scratch.mit.edu/login/", data=json.dumps({"username": username, "password": password}), headers=headers, cookies={"scratchcsrftoken": "a", "scratchlanguage": "en"})
            response = response.headers["Set-Cookie"]).group()
            self.username = username
            self.session_id = re.search('"(.*)"', response)
            return _login()
        except AttributeError:
            raise LoginError("Your login data was wrong. Check if you spelled your credits correctly, or if you are in replit, see the docs for more information.")
        
    def CloudConnection(self, project_id: int):
        return _cloud.CreateCloudConnection(project_id=project_id, session=self)

    def ConnectProject(self, id: int):
        return _project.CreateConnectProject(id=id, session=self)

    def ManageSettings(self):
        return _settings.ManageSettings(session=self)

def Login(username: str, password: str):
    return Session._login_pass(username=username, password=username)
