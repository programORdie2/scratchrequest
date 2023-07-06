import warnings
from ._exceptions import LoginError
from . import _cloud
import requests, json, re

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    "x-csrftoken": "a",
    "x-requested-with": "XMLHttpRequest",
    "referer": "https://scratch.mit.edu",
}

class Session:
    def __init__(self, username : str=None, *, session_id : str):
        self.session_id = session_id
        self.username = username
        self.headers = headers
        self._login()

    def _login(self):
        '''
        Don't use this
        '''
        self.cookies = {
            "scratchcsrftoken" : "a",
            "scratchlanguage" : "en",
            "scratchpolicyseen": "true",
            "scratchsessionsid" : self.session_id,
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        account = requests.post("https://scratch.mit.edu/session", headers=self.headers, cookies={
            "scratchsessionsid": self.session_id,
            "scratchcsrftoken": "a",
            "scratchlanguage": "en",
        }).json()
        try:
            self.xtoken = account["user"]["token"]
            self.headers["X-Token"] = self.xtoken
        except KeyError:
            raise LoginError("Your login data was wrong. Check if you spelled your credits correctly, or if you are in replit, see the docs for more information.")

    @classmethod
    def login(cls, username : str, password : str):
        '''
        Login from your username and password.
        '''
        try:
            return cls(
                username, session_id=str(re.search('"(.*)"', requests.post(
                    "https://scratch.mit.edu/login/",
                    data=json.dumps({
                        "username": username,
                        "password": password
                    }),
                    headers=headers,
                    cookies={
                        "scratchcsrftoken": "a",
                        "scratchlanguage": "en"
                    }
                ).headers["Set-Cookie"]).group())
            )
        except AttributeError:
            raise LoginError("Your login data was wrong. Check if you spelled your credits correctly, or if you are in replit, see the docs for more information.")
        except Exception as e:
            raise Exception("An error occurred while trying to log in.") from e
        
    def CloudConnection(self, project_id : int, **kwargs) -> _cloud.CreateCloudConnection:
        '''
        Create a cloud connection to a project.
        '''
        return _cloud.CreateCloudConnection(project_id=project_id, session=self, **kwargs)
