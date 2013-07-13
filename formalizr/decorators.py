import json
import urlparse

from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME


def ajax_login_required(view_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)

        if request.is_ajax():
            data = json.dumps({
                'status': 'error',
                'error': 'Unauthorized',
                'messages': [{'message': _('Not authorized!'), 'level': 'error'}]
            })
            return HttpResponse(data, mimetype='application/json', status=401)
        else:
            path = request.build_absolute_uri()
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse.urlparse(login_url or
                                                           settings.LOGIN_URL)[:2]
            current_scheme, current_netloc = urlparse.urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(path, login_url, redirect_field_name)
    wrap.__doc__ = view_func.__doc__
    wrap.__dict__ = view_func.__dict__
    return wrap
