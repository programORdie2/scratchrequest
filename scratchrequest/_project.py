import requests, json
from ._exceptions import AuthError, UploadError, DownloadError, ProjectNotFound

class CreateConnectProject:
  def __init__(self, id: str, session=None):
    self.id = id
    if session == None:
      self.username = None
    else:    
      self.username = session.username
      self.session_id = session.session_id
      self.csrf_token = session.csrf_token
      self.xtoken = session.xtoken
      self.json_headers = {"x-csrftoken": self.csrf_token, "X-Token": self.xtoken, "x-requested-with": "XMLHttpRequest", "Cookie": f"scratchcsrftoken={self.csrf_token};scratchlanguage=en;scratchsessionsid={self.session_id};", "referer": f"https://scratch.mit.edu/projects/{self.id}/", "accept": "application/json", "Content-Type": "application/json"}    
    self.update_data()

  def _get_all_data(self):
    try:
      self._all_data = requests.get(f'https://api.scratch.mit.edu/projects/{self.id}/').json()
      self._all_data['id']
    except KeyError:
      raise ProjectNotFound('The projectID you enterd does not exists or is unshared.')
    return self._all_data

  def update_data(self):
    d = self._get_all_data()
    self.title = d['title']
    self.author = d['author']['username']
    self.views = d['stats']['views']
    self.loves = d['stats']['loves']
    self.favorites = d['stats']['favorites']
    self.remixes = d['stats']['remixes']
    self.remix = d['remix']
    self.description = d['description']
    self.instructions = d['instructions']
    self.comments_allowed = d['comments_allowed']
    self.created = d['history']['created']
    self.modified = d['history']['modified']
    self.shared = d['history']['shared']
    self.thumbnail_url = d['image']

  def upload_json(self, project_json: str):
    if self.username == None:
      raise AuthError('You need to be logged in to upload a project.')
    if self.username != self.author:
      raise AuthError('You need to be the owner of the project to upload data.')
    request = requests.put(f"https://projects.scratch.mit.edu/{self.id}", headers=self.json_headers, data=project_json)
    if request.status_code != 200:
      raise UploadError(f'Failed to upload project - code {response.status_code}')

  def get_json(self):
    token = self._all_data['project_token']
    response = requests.get(f"https://projects.scratch.mit.edu/{self.id}?token={token}")
    if response.status_code != 200:
      raise DownloadError(f'Failed to download project - status code {response.status_code}')
    return response.content

  def download(self, path: str='./project.sb3'):
    json = self.get_json()
    file = path.replace('.sb3', '')
    file = file + '.sb3'
    open(file, 'wb').write(json)

  def upload(self, path: str):
    p_json = open(path, 'rb').read()
    self.upload_json(p_json)

  def set_title(self, title: str):
    if self.username == None:
      raise AuthError('You need to be logged in to set the title.')
    if self.username != self.author:
      raise AuthError('You need to be the owner of the project to set the title.')
    data = json.dumps({'title': title})
    request = requests.put(f"https://api.scratch.mit.edu/projects/{self.id}", headers=self.json_headers, data=data)
    if request.status_code != 200:
      raise ProjectError(f'Failed to set title - code {response.status_code}')

  def set_description(self, description: str):
    if self.username == None:
      raise AuthError('You need to be logged in to set the description.')
    if self.username != self.author:
      raise AuthError('You need to be the owner of the project to set the descriptionn.')
    data = json.dumps({'description': description})
    request = requests.put(f"https://api.scratch.mit.edu/projects/{self.id}", headers=self.json_headers, data=data)
    if request.status_code != 200:
      raise ProjectError(f'Failed to set description - code {response.status_code}')

  def set_instructions(self, instructions: str):
    if self.username == None:
      raise AuthError('You need to be logged in to set the instructions.')
    if self.username != self.author:
      raise AuthError('You need to be the owner of the project to set the descriptionn.')
    data = json.dumps({'instructions': instructions})
    request = requests.put(f"https://api.scratch.mit.edu/projects/{self.id}", headers=self.json_headers, data=data)
    if request.status_code != 200:
      raise ProjectError(f'Failed to set description - code {response.status_code}')
