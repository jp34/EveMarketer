from api.server.data.data_manager import DataManager
from api.server.request_handler import RequestHandler
from http.server import HTTPServer
import threading
import webbrowser
import os


class EveServer:

    def __init__(self):
        self.manager = DataManager()

        self.host = self.manager.get_host()
        self.port = self.manager.get_port()
        self.address = (self.host, self.port)
        self.callback = self.manager.get_callback()
        self.client_id = self.manager.get_client_id()
        self.state = self.manager.get_state()
        self.challenge = self.manager.get_challenge()
        self.verifier = self.manager.get_verifier()
        self.base_url = self.manager.get_base_url()
        self.scope = self.manager.get_scope()

        self.server = HTTPServer(self.address, RequestHandler)
        self.listening = False


    def start(self):
        input_thread = threading.Thread(target=self.listen)
        input_thread.start()
        self.listening = True
        print("[Server] Now listening on port", self.port)


    def listen(self):
        self.server.serve_forever()
    

    def authorize(self):
        if self.listening:
            sso_url = self.get_auth_link()
            webbrowser.open(sso_url)
            print("[Server] Started sso authorization")
        else:
            print("[Server] Start packet server before auth")


    def get_auth_link(self):
        return f"{self.base_url}authorize/?response_type=code&redirect_uri={self.callback}" \
               f"&client_id={self.client_id}&scope={self.scope}&code_challenge={self.challenge}" \
               f"&code_challenge_method=S256&state={self.state}"
