#!/usr/bin/env python 
#-*-coding:utf8-*-
import datetime
import tornado.auth
import tornado.web
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

def timestamptodate(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

class Template():

    """
    A simple class to hold methods for rendering templates.
    """
    def render_template(self, template_name, **kwargs):
        template_dirs = []
        if self.settings.get('template_path', ''):
            template_dirs.append(
                self.settings["template_path"]
            )

        env = Environment(loader=FileSystemLoader(template_dirs))
        #env.filters['region_descript'] = region_descript
        #env.filters['timestamptodate'] = timestamptodate
        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(kwargs)
        return content


class BaseHandler(tornado.web.RequestHandler, Template):
    """
    RequestHandler already has a `render()` method. I'm writing another
    method `render2()` and keeping the API almost same.
    """

    def get_template_namespace(self):
        """Returns a dictionary to be used as the default template namespace.

        May be overridden by subclasses to add or modify values.

        The results of this method will be combined with additional
        defaults in the `tornado.template` module and keyword arguments
        to `render` or `render_string`.
        """
        namespace = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            locale=self.locale,
            _=self.locale.translate,
            pgettext=self.locale.pgettext,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.reverse_url,
            userlevel=self.userlevel   #adding
        )
        namespace.update(self.ui)
        return namespace

    @property
    def userlevel(self):
        if self.current_user:
            return int(getOneInfo('accounts',{"username":self.current_user})['level'])
        return -1
        
    def get_current_user(self):
        return self.get_secure_cookie("username")

    def render2(self, template_name, **kwargs):
        """
        This is for making some extra context variables available to the template.
        """
        kwargs.update({
            'settings': self.settings,
            'STATIC_URL': self.settings.get('static_url_prefix', '/static/'),
            'request': self.request,
            'xsrf_token': self.xsrf_token,
            'xsrf_form_html': self.xsrf_form_html,
        #    'current_user':self.current_user
        })
        current_user = self.get_current_user()
        content = self.render_template(template_name,current_user = current_user,eval = eval,**kwargs)
        self.write(content)

    def template(self, template_name, **kwargs):
        kwargs.update({
            'settings': self.settings,
            'STATIC_URL': self.settings.get('static_url_prefix', '/static/'),
            'request': self.request,
            'xsrf_token': self.xsrf_token,
            'xsrf_form_html': self.xsrf_form_html,
        })
        content = self.render_template(template_name, **kwargs)
        return content
    
    def uri(self):
        return self.request.uri

    @property
    def is_api_request(self):
        return True if self.uri().startswith('/api') else False



                      
