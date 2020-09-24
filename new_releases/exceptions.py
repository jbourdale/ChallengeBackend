from rest_framework.exceptions import APIException


class SpotifyTokenRequestInvalidException(APIException):
    status_code=400
    default_detail = "Invalid request while login to spotify"
    default_code = "Unable to login"
