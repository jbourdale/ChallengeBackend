class SpotifyToken():
    def __init__(self, token, expires_in, token_type):
        self.token = token
        self.expires_in = expires_in
        self.token_type = token_type

    def get_header(self):
        return {
            'Authorization': f'{self.token_type} {self.token}'
        }
