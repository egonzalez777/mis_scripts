import oauth2 as oauth

from urllib import urlencode
import hashlib

import random

# TODO: Create test cases for all functionality.


API_ROOT = "https://api.linkedin.com/"
API_VERSION = "v1"
API_ENDPOINTS = {

}

class LinkedinException(Exception):
    pass


class LinkedinAPI(object):
    """Method sig: (key, secret, redirect)"""

    AUTHORIZATION_URL = 'https://www.linkedin.com/uas/oauth2/authorization'
    TOKEN_ACCESS_URL = 'https://www.linkedin.com/uas/oauth2/accessToken'
    client = None
    consumer = None
    consumer_key = None
    consumer_secret = None

    def __init__(self,
                 consumer_key,
                 consumer_secret,
                 redirect):
        """Method sig: (key, secret, redirect)"""

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.redirect = redirect

        self.consumer = oauth.Consumer(
            key=self.consumer_key,
            secret=self.consumer_secret)
        self.client = oauth.Client(self.consumer)

    @property
    def get_auth_url(self):
        """Generates authorization url."""

        return '%s?%s' % (self.AUTHORIZATION_URL, self.authorization_body())

    def authorization_body(self):
        """Creates the authorization POST params."""

        self.authorization_body = urlencode({
            'response_type': 'code',
            'client_id': self.consumer_key,
            'redirect_uri': self.redirect,
            'state': str(self._generate_random_string()),
        })

        return self.authorization_body

    def get_access_token(self, access_code, redirect_uri):
        if access_code:
            # Execute the following code that retrieves the access Token.
            request_params = {
                'grant_type': 'authorization_code',
                'code': access_code,
                'redirect_uri': redirect_uri,
                'client_id': self.consumer_key,
                'client_secret': self.consumer_secret,
            }
            resp, content = self.client.request(
                self.TOKEN_ACCESS_URL,
                "POST",
                body=urlencode(request_params))

            print resp
            print content
            print self.authorization_body
        else:
            raise LinkedinException("Missing access code.")

    def _generate_random_string(self):
        return hashlib.md5(
            '%s%s' % (
                random.uniform(1, 32) ** 32, self.consumer_secret)).hexdigest()
