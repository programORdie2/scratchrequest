import ssl
import json
import websocket
from ssl import SSLEOFError, SSLError

from . import _exceptions

class TWCloudConnection:
    def __init__(self, project_id: int, username: str):
        """
        Main class to connect turbowarp cloud variables
        """
        self.project_id = project_id
        self.username = username
        self._cloud_d = None
        self._make_connection()

    def _send_packet(self, packet):
        """
        Don't use this
        """
        self._ws.send(json.dumps(packet) + "\n")

    def _make_connection(self):
        """
        Don't use this
        """
        self._ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
        self._ws.connect("wss://clouddata.turbowarp.org",
                         origin="https://turbowarp.org",
                         enable_multithread=True)
        self._send_packet(
            {
                "method": "handshake",
                "user": self.username,
                "project_id": str(self.project_id),
            }
        )

    def get_var_data(self) -> list:
        """
        Returns the cloud variable data
        """
        #self._cloud_d = self._ws.recv()
        data = []
        for d in self._cloud_d.split("\n"):
            one = json.loads(d)
            if one["name"] != "☁ @scratchrequests":
                data.append(one)
        if len(data) == 0:
            return None
        return data

    def get_var(self, name: str, limit: int=256) -> list:
        value = []
        data = self.get_var_data()
        for d in data:
            if d["name"] == f"☁ {name}":
                value.append(d["value"])
        return value[0:limit]

    def set_cloud_variable(self, name: str, value: int | str) -> bool:
        """
        Set a cloud variable
        :param variable_name: Variable name
        :param value: Variable value
        """
        if str(value).isdigit() and value == '':
            raise Exceptions.InvalidCloudValue(f"The Cloud Value should be a set of digits and not '{value}'!")

        try:
            if len(str(value)) > 256:
                raise ValueError(
                    "Turbowarp has Cloud Variable Limit of 256 Characters per variable. Try making the value shorter!")
            if str(name.strip())[0] != "☁":
                n = f"☁ {name.strip()}"
            else:
                n = f"{name.strip()}"
            packet = {
                "method": "set",
                "name": n,
                "value": str(value),
                "user": self.username,
                "project_id": str(self.project_id),
            }
            self._send_packet(packet)
            self._cloud_d = self._ws.recv()
            return True
        except (ConnectionAbortedError, BrokenPipeError, SSLEOFError, SSLError):
            self._make_connection()
            return False

