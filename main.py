#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import logging
import json
import os
import utils
from google.appengine.ext.webapp import template
from models import Project


class MainHandler(utils.BaseHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, template_values))


class ProjectHandler(utils.APIRequest):
    def get(self):
        projects = Project.query().fetch()
        self.response.write(json.dumps(self.to_json(projects)))

    def post(self):
        p = Project()
        p.owner = self.request.get('owner').upper()
        p.description = self.request.get("description")
        p.folder = self.request.get("folder")
        p.name = self.request.get("name")
        p.status = self.request.get("status")
        p.put()
        self.response.write(json.dumps(self.to_json(p)))
with open('key.json') as f:
     json_data = json.load(f)
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': json_data['secret_key'],
}
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/projects', ProjectHandler)
], debug=True, config=config)
