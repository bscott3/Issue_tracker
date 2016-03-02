import webapp2
import json
import os
from google.appengine.ext import ndb
from datetime import datetime
import logging, base64
from google.appengine.api import app_identity
from google.appengine.api import mail
from google.appengine.api import users
import webapp2

from webapp2_extras import sessions


DEFAULT_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def login_required(handler_method):

    def wrapper(self, *args, **kwargs):
        user = users.get_current_user()
        if user:
            # Google login
            handler_method(self, *args, **kwargs)
        else:
            logging.debug('Redirecting to login url')
            self.redirect(users.create_login_url(self.request.url))

    return wrapper


class APIRequest(webapp2.RequestHandler):
    def __init__(self, request, response):
        # super(APIRequest, self).__init__()  # pycharm really wants me to add this
        self.initialize(request=request, response=response)

    def to_json(self, o):
        if isinstance(o, list):
            return [self.to_json(l) for l in o]
        if isinstance(o, dict):
            x = {}
            for l in o:
                x[l] = self.to_json(o[l])
            return x
        if isinstance(o, datetime):
            return o.strftime(DEFAULT_TIME_FORMAT)
        if isinstance(o, ndb.GeoPt):
            return {'lat': o.lat, 'lon': o.lon}
        if isinstance(o, ndb.Key):
            return o.urlsafe()
        if isinstance(o, ndb.Model):
            dct = o.to_dict()
            dct['datastore_id'] = o.key.id()
            return self.to_json(dct)
        return o

    def options(self):
        self.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
        self.response.set_status(200)

    def check_params(self, params):
        for param in params:
            if param not in self.request.params:
                self.abort(code=400,
                           detail="Missing parameter: {param}.".format(param=param))

    def check_body(self, fields):
        if self.request.body:
            body = json.loads(self.request.body)
            missing_fields = []
            for field in fields:
                if field not in body:
                    missing_fields.append(field)
            if missing_fields:
                self.abort(code=400,
                           detail="Missing Fields: {missing_fields}".format(missing_fields=missing_fields))
            else:
                return body
        else:
            self.abort(code=400,
                       detail="Request body not found.")


def send_failure_summary(exception):
    try:
        sender = "failure@{ident}.appspotmail.com".format(ident=app_identity.get_application_id())
        mail.send_mail_to_admins(sender=sender,subject="Error", body="There was a unhandled exception in the sending of "
                                                    " %s" % exception)
    except mail.InvalidEmailError, e:
        logging.error("Unable to send failure email to application admins %s" % e)
    except Exception, e:
        logging.error("Unknown exception sending failure summary to admins %s" % e)


def isDev():
    is_dev = False
    iden = app_id = os.environ['APPLICATION_ID']
    if 'dev' in iden:
        is_dev = True
        return is_dev
    else:
        return is_dev

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session(backend='memcache')