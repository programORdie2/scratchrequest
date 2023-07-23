import requests, json

class ManageSettings:
  def __init__(self, session):
    self.session = session
    self.json_headers = {"x-csrftoken": self.session.csrf_token, "X-Token": self.session.xtoken, "x-requested-with": "XMLHttpRequest", "Cookie": f"scratchcsrftoken={self.session.csrf_token};scratchlanguage=en;scratchsessionsid={self.session.session_id};", "referer": "https://scratch.mit.edu/"}
    self.url = ''

  def check_password(self, password: str):
    data = {"csrfmiddlewaretoken": self.session.csrf_token, "password": password,}
    response = requests.post(self.url + "https://scratch.mit.edu/accounts/check_password",data=json.dumps(data),headers=self.json_headers).json()
    return response['succes']

  def change_country(self, country: str):
    data = {'csrfmiddlewaretoken': self.session.csrf_token, 'country': country}
    return requests.post(self.url + 'https://scratch.mit.edu/accounts/settings/', data=data, headers=self.json_headers)

  def change_password(self, old_password: str, new_password: str):
    data = {"csrfmiddlewaretoken": self.session.csrf_token, "old_password": old_password, "new_password1": new_password, "new_password2": new_password}
    return requests.post(url + 'https://scratch.mit.edu/accounts/password_change/', data=data, headers=self.json_headers)

  def change_email(self, new_email: str, password: str):
    data = {"csrfmiddlewaretoken": self.session.csrf_token, "email_address": new_email, "password": password}
    return requests.post(url + 'https://scratch.mit.edu/accounts/email_change/', data=data, headers=self.json_headers)

  def change_email_subscription(self, activites: bool=False, teacher_tips: bool=False):
    data = {"csrfmiddlewaretoken": self.session.csrf_token}
    if activities:
      data["activites"] = "on"
    if teacher_tips:
      data["teacher_tips"] = "on"
    return requests.post(url + 'https://scratch.mit.edu/accounts/settings/update_subscription/', data=data, headers=self.json_headers)
