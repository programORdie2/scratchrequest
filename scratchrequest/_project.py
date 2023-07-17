import requests
from ._exceptions import AuthError, UploadError, DownloadError, ProjectNotFound

class CreateConnectProject:
  def __init__(self, id: str, session=None):
    if session == None:
      username = None
    else:    
      self.username = session.username
      self.session_id = session.session_id
      self.csrf_token = session.csrf_token
      self.xtoken = session.xtoken
    self.id = id
    self._get_all_data()

  def _get_all_data(self):
    try:
      self._all_data = requests.get(f'https://api.scratch.mit.edu/projects/{self.id}/').json()
      self._all_data['id']
    except KeyError:
      raise ProjectNotFound('The projectID you enterd does not exists or is unshared.')

  def upload_json(self, project_json: str):
    if self.username == None:
      raise AuthError('You need to be logged in to upload a project.')
    headers = {"x-csrftoken": self.csrf_token, "X-Token": self.xtoken, "x-requested-with": "XMLHttpRequest", "Cookie": f"scratchcsrftoken={self.csrf_token};scratchlanguage=en;scratchsessionsid={self.session_id};", "referer": f"https://scratch.mit.edu/projects/{self.id}/", "accept": "application/json", "Content-Type": "application/json"}
    request = requests.put(f"https://projects.scratch.mit.edu/{self.id}", headers=headers, data=project_json)
    if request.status_code != 200:
      raise UploadError(f'Failed to upload project - status code {request.status_code}')

  def get_json(self):
    token = self._all_data['project_token']
    response = requests.get(f"https://projects.scratch.mit.edu/{self.id}?token={token}")
    if response.status_code != 200:
      raise DownloadError(f'Failed to download project - status code {response.status_code}')
    return response.content

  def download(self, file: str='./project.sb3'):
    json = self.get_json()
    file = file.replace('.sb3', '')
    file = file + '.sb3'
    open(file, 'wb').write(json)
