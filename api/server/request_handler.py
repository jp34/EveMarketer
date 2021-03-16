from api.server.data.data_manager import DataManager
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import requests
import base64
import json


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """
        Handles GET requests and calls the appropriate handler
        
        Input: None
        Ouput: None
        """
        # Print get information to console
        self.log_get()

        # Handle GET request
        parsed = self.path.split("/")

        if parsed[1] == 'auth':
            # Case: User auth redirected from login.eveonline.com
            self.handle_auth()


    def handle_auth(self):
        """
        Organizes the process of authorizing to login.eveonline.com

        Input: None
        Output: None
        """
        manager = DataManager()

        # Authorization code recieved from GET url
        auth_code, state = self.parse_auth_path()

        # Response from token request
        token_request = self.request_token(auth_code, state)
        
        # Dictionary containing access and refresh tokens
        token_dict = self.handle_token_response(token_request)

        if token_dict:
            manager.update_token(token_dict)


    def parse_auth_path(self):
        """
        Function is called when request contains an authorization code from
        login.eveonline.com. It parses and returns the code and state parameter
        from the path of the response.

        Input: None
        Output:
            - auth_code : string containing an authorization code from
                          login.eveonline.com
            - state : string of random characters, paramater recieved from
                      login.eveonline.com
        """
        path_parsed = self.path.split("/")
        path_data = path_parsed[2].split("&")
        auth_code = path_data[0][6:]
        state = path_data[1][6:]

        return auth_code, state
    

    def request_token(self, auth_code, state):
        """
        Makes a post request to login.eveonline.com with auth_code. Response will contain
        an access token.

        Input:
            - auth_code : string of characters, authorization code received from
                          login.eveonline.com
            - state : sting of characters, state recieved from login.eveonline.com
        Output:
            - response : requests.models.Response object, containing a token recieved from
                         login.eveonline.com
        """
        manager = DataManager()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "login.eveonline.com",
        }

        body = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "client_id": manager.get_client_id(),
            "code_verifier": manager.get_verifier()
        }

        response = requests.post(
            "https://login.eveonline.com/v2/oauth/token",
            data=body,
            headers=headers,
        )

        self.log_post(response)
        return response
    

    def handle_token_response(self, response):
        """
        Returns a dictionary taken from a request response. Returns false if the request
        results in an error.

        Input:
            - response : requests.models.Response object
        Output:
            - token_dict : dictionary containing access and refresh tokens
        """
        if response.ok:
            response_content = response.content.decode('utf-8')
            token_dict = json.loads(response_content)
            return token_dict
        else:
            return False


    def log_get(self):
        """
        Prints relevent data from self to the console
        
        Input: None
        Output: None
        """
        print(f"[Server][GET]  => Host: {self.client_address[0]} Port: {self.client_address[1]}")
        print(f"               => Path: {self.path}")
        print('\n')


    def log_post(self, response):
        """
        Prints relevent data from response object to the console

        Input:
            - response : requests.models.Response object
        Output: None
        """
        headers = dict(response.headers)
        print(f"[Server][POST] => Code: {response.status_code}")
        print(f"               => Content Type: {headers['Content-Type']}")
        print(f"               => Url: {response.url}")
        print(f"               => Date: {headers['Date']}")
        print('\n')
