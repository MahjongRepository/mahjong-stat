from django.http import HttpResponse
from functools import wraps

from api.models import ApiToken


def token_authentication(view_func):

    def _checklogin(request, *args, **kwargs):
        token_string = request.META.get('HTTP_TOKEN')

        token = ApiToken.objects.filter(token=token_string)
        if not token.exists():
            return HttpResponse('Unauthorized', status=401)

        token = token.first()
        request.user = token.user

        return view_func(request, *args, **kwargs)

    return wraps(view_func)(_checklogin)
