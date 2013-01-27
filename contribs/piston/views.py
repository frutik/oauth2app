from oauth2app.token import TokenGenerator
from django.views.decorators.http import require_POST
import logging

@require_POST
def token(request):
    try:
        authorizer = TokenGenerator()
    except Exception, e:
        logging.debug(e)
        raise e
    else:
        return authorizer(request)
