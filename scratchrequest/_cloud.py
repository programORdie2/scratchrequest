from typing import Literal, Union
from ._exceptions import QuickAccessDisabledError
from websocket import WebSocket
from threading import Thread
import json, math, time, requests

NoneType = type(None)

class Event:
    def __init__(self, type : Literal["set", "delete", "connect", "create"], **entries):
        entries["type"] = type
        self.__dict__.update(entries)

    @property
    def data(self):
        if not "var" in self.__dict__:
            raise Exception("No setting")
        if not "_data" in self.__dict__:
            self._data = list(filter(lambda x: x["value"] == self.value, self.project.get_cloud_logs(project_id=self.project.project_id, filter_by_name=self.var, filter_by_name_literal=True)))[0]
        return self._data

    @property
    def user(self):
        return self.data["user"]

    @property
    def timestamp(self):
        return self.data["timestamp"]

class CreateCloudConnection:
    def __init__(self, *, project_id : int, session = None, username : str = None, quickaccess : bool = False, reconnect : bool = True, receive_from_websocket : bool = True):
        self.project_id = project_id
        self.session = session
        self.username = username if username is not None else session.username
        self.quickaccess = quickaccess
        self.reconnect = reconnect
        self.host = ""
        self.values = {}
        self.events = {}
        self.wait_until = 0
        self.receive_from_websocket = receive_from_websocket
        self.data_reception = None
        self._connect()
        if not self.receive_from_websocket:
            while True:
                try:
                    self.receive_new_data()
                    break
                except:
                    self._connect()
            return
        self.data_reception = Thread(target=self.receive_data)
        self.data_reception.start()

    def enable_quickaccess(self):
        '''
        Use for enabling the use of the object as a lookup table.
        '''
        self.quickaccess = True

    def disable_quickaccess(self):
        '''
        Use for disabling the use of the object as a lookup table.
        '''
        self.quickaccess = False

    def _connect(self, *, retry : int = 10):
        '''
        Don't use this.
        '''
        try:
            self.websocket = WebSocket()
            self.websocket.connect(
                "wss://clouddata.scratch.mit.edu",
                cookie="scratchsessionsid=" + self.session.session_id + ";",
                origin="https://scratch.mit.edu",
                enable_multithread=True,
            )
            self.handshake()
            self.emit_event("connect", timestamp=time.time())
        except Exception as e:
            if retry == 1:
                raise ConnectionError(f"There was an error while connecting to the cloud server: {e}")
            self._connect(retry=retry - 1)

    def handshake(self):
        self.send_packet(
                {
                    "method": "handshake",
                    "user": self.username,
                    "project_id": self.project_id
                }
            )

    def send_packet(self, packet):
        '''
        Don't use this.
        '''
        self.websocket.send(json.dumps(packet) + "\n")

    @staticmethod
    def get_cloud_logs(*, project_id : str, limit : int = 100, filter_by_name : Union[str, NoneType] = None, filter_by_name_literal : bool = False) -> list:
        '''
        Use for getting the cloud logs of a project.
        '''
        logs = []
        filter_by_name = filter_by_name if filter_by_name_literal else "☁ " + filter_by_name.replace("☁ ", "", 1) if filter_by_name else None
        offset = 0
        while len(logs) < limit:
            data = requests.get(f"https://clouddata.scratch.mit.edu/logs?projectid={project_id}&limit={limit}&offset={offset}").json()
            logs.extend(data if filter_by_name is None else filter(lambda x: x["name"] == filter_by_name, data))
            offset += len(data)
            if len(data) == 0:
                break
        return logs[:limit]

    @staticmethod
    def verify_value(value : Union[float, int, bool, NoneType]):
        '''
        Use for detecting if a  value can be used for cloud variables.
        '''
        try:
            assert not isinstance(value, Union[str, list, dict, tuple]) or isinstance(float(value), float)
            assert len(json.dumps(value)) <= 256
        except Exception as e:
            raise ValueError("Bad value for cloud variables.") from e

    def _set_variable(self, *, name : str, value : Union[float, int, bool, NoneType], retry : int):
        '''
        Don't use this.
        '''
        try:
            self.send_packet(
                {
                    "method": "set",
                    "name": name,
                    "value": value,
                    "user": self.username,
                    "project_id": self.project_id,
                }
            )
        except ConnectionError as e:
            raise e
        except:
            if not self.reconnect:
                raise ConnectionError("There was an error while setting the cloud variable.")
            if retry == 1:
                raise ConnectionError("There was an error while setting the cloud variable.")
            self._connect()
            self._set_variable(name=name, value=value, retry=retry - 1)

    def set_variable(self, *, name : str, value : Union[float, int, bool, NoneType], name_literal : bool = False):
        '''
        Use for setting a cloud variable.
        '''
        self.verify_value(value)
        name = name if name_literal else "☁ " + name.replace("☁ ", "", 1)
        time.sleep(max(0, self.wait_until - time.time()))
        self.wait_until = time.time() + 0.1

        self._set_variable(name=name, value=value, retry=10)
        self.emit_event("set", name=name.replace("☁ ", "", 1), var=name, value=value, timestamp=time.time())

    def get_var_data(self, name : str):
        name = name.replace('☁ ', '', 1)
        response = requests.get(f"https://clouddata.scratch.mit.edu/logs?projectid={self.project_id}&limit=100&offset=0").json()
        response = list(filter(lambda k: k['name'] == '☁ '+name, response))
        if response == []:
          return None
        response = response[0]
        re = {"value": str(response['value']), "user": str(response['user']), "timestamp": str(response["timestamp"])}
        return re

    def get_var(self, name: str):
        _all_cloud = self.get_var_data(name=name)
        if _all_cloud == None:
          return None
        _val = _all_cloud['value']
        return _val

    def __getitem__(self, item : str) -> Union[float, int, bool, NoneType]:
        if not self.quickaccess:
            raise QuickAccessDisabledError("Quickaccess is disabled")
        return self.get_var(name=item)

    def __setitem__(self, item : str, value : Union[float, int, bool, NoneType]):
        if not self.quickaccess:
            raise QuickAccessDisabledError("Quickaccess is disabled")
        self.set_variable(name=item, value=value)
    
    def receive_new_data(self, first : bool = False) -> dict:
        '''
        Use for receiving new cloud data.
        '''
        data = [json.loads(j) for j in self.websocket.recv().split("\n") if j]
        changed = [i["name"] for i in data if i["method"] == "set" and i["name"] in self.values]
        self.values.update({i["name"]: i["value"] for i in data if i["method"] == "set"})
        for i in data:
            i.pop("project_id")
            i["var"] = i["name"]
            i["name"] = i["name"].replace("☁ ", "", 1)
            if not first or i["name"] in changed:
                self.emit_event(i.pop("method"), **i)
        return self.values

    def receive_data(self):
        '''
        Use for receiving cloud data.
        '''
        while True:
            try:
                self._connect()
                self.receive_new_data(first=True)
                break
            except: pass
        while True:
            try:
                self.receive_new_data()
            except Exception as e:
                while True:
                    try:
                        self._connect()
                        self.receive_new_data(first=True)
                        break
                    except: pass

    def emit_event(self, event : Union[Literal["set", "delete", "connect", "create"], Event], **entries) -> int:
        '''
        Use for emitting events. Returns how many handlers could handle the event.
        '''
        data = event if isinstance(event, Event) else Event(event, **entries)
        data.project = self
        if isinstance(event, Event):
            event = event.type
        return self._emit_event(event, data) + self._emit_event("any", data)

    def _emit_event(self, event : Literal["set", "delete", "connect", "create", "any"], data : Event) -> int:
        '''
        Don't use this.
        '''
        amount = 0
        if not event in self.events:
            return 0
        for i in self.events[event]:
            try:
                i(data)
                amount += 1
            except: pass
        return amount

    def on(self, event : Literal["set", "delete", "connect", "create", "any"]):
        '''
        Register a new event.
        '''
        def wrapper(func):
            if event in self.events:
                eventlist = self.events[event]
            else:
                eventlist = self.events[event] = []
            eventlist.append(func)
        return wrapper
