#!/usr/bin/env python
#-*-coding:utf8-*-


import functools
try:
    import urlparse  # py2
except ImportError:
    import urllib.parse as urlparse  # py3
try:
    from urllib import urlencode  # py2
except ImportError:
    from urllib.parse import urlencode  # py3

from tornado.web import HTTPError
ops=['luopeng1','zhaoyiding','wangyuzu']


def authenticated(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.

    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET", "POST"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                return self.redirect(url)
            raise HTTPError(403, "登录失败")
        else:
            self._ = self.get_query_argument('_','')
            if self.request.method == "GET":
                if self._ == 'delete':
                    if self.current_user not in ops:
                        self.render2("assets/error.html",err_msg='无删除权限')
                        if not self._finished: self.finish()
                        raise HTTPError(401,'没有删除权限')
            elif self.request.method == "POST":
                if self.current_user not in ops:
                    self.render2("assets/error.html",err_msg='无权限')
                    if not self._finished: self.finish()
                    raise HTTPError(402,'没有权限')
        return method(self, *args, **kwargs)
    return wrapper

