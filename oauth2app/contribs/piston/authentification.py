from oauth2app.authenticate import JSONAuthenticator, AuthenticationException, InvalidToken, InvalidRequest, InsufficientScope
from oauth2app.exceptions import OAuth2Exception
from oauth2app.models import AccessRange

import logging

SCOPE_KEY = 'client_api'

class OAuth2Authentication(object):
    """
    Piston compatible OAuth 2.0 authenticator.
    """

    def is_authenticated(self, request):
        """
        Checks whether a means of specifying authentication
        is provided, and if so, if it is a valid token.

        Read the documentation on `HttpBasicAuthentication`
        for more information about what goes on here.
        """

        try:
            scope = AccessRange.objects.get(key=SCOPE_KEY)
        except AccessRange.DoesNotExist:
            logging.warn(u'Missing API scope: ' + SCOPE_KEY)
            return False

        try:
            authenticator = JSONAuthenticator(scope)
        except OAuth2Exception:
            self.authentificator = authenticator
            return False

        try:
            authenticator.validate(request)
        except (AuthenticationException, InvalidToken, InvalidRequest, InsufficientScope):
            self.authentificator = authenticator
            return False

        if not authenticator.valid:
            return False

        request.user = authenticator.user
        return True

    def challenge(self):
        """
        Not authentificated request. Client must create auth token first ant use it.
        """
        try:
            return self.authentificator.error_response()
        except:
            return None
