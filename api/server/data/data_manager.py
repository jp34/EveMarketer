from api.server.data.json_manager import JSONManager
import base64
import secrets
import hashlib


class DataManager:

    def __init__(self):
        self.manager = JSONManager()


    # Getters for client.json    
    def get_host(self):
        return self.manager.get_data('client', 'host')
    

    def get_port(self):
        return self.manager.get_data('client', 'port')


    def get_callback(self):
        return self.manager.get_data('client', 'callback')
    

    def get_client_id(self):
        return self.manager.get_data('client', 'client_id')
    

    def get_state(self):
        return self.manager.get_data('client', 'state')
    

    def get_challenge(self):
        return self.manager.get_data('client', 'challenge')
    

    def get_verifier(self):
        return self.manager.get_data('client', 'verifier')
    

    def get_base_url(self):
        return self.manager.get_data('client', 'base_url')
    

    def get_scope(self):
        return self.manager.get_data('client', 'scope')
    

    # Getters for token.json
    def get_access_token(self):
        return self.manager.get_data('token', 'scope')
    

    def get_refresh_token(self):
        return self.manager.get-data('token', 'scope')
    
    
    def update_token(self, new_token):
        self.manager.write_json('token', new_token)
    

    def new_challenge(self):
        challenge, verifier = self.new_challenge()
        self.manager.update_json('client', 'challenge', challenge)
        self.manager.update_json('client', 'verifier', verifier)


    @staticmethod
    def build_challenge(self):
        random_string = secrets.token_bytes(32)
        random = self.url_encode(random_string)
        verifier = random
        m = hashlib.sha256()
        m.update(random)
        d = m.digest()
        challenge = base64.urlsafe_b64encode(d).decode().replace("=", "")
        return challenge, verifier
    

    @staticmethod
    def url_encode(data):
        return base64.urlsafe_b64encode(data.encode('utf-8'))
    

    @staticmethod
    def url_decode(data):
        return base64.decodestring(data)
