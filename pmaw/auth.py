from requests.auth import AuthBase


class Authenticator(AuthBase):

    def __init__(self, access_token):
        self.access_token = access_token

    def __call__(self, r):
        if self.access_token is not None:
            r.headers['x-messari-api-key'] = self.access_token
        return r
