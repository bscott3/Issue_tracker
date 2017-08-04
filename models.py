from google.appengine.ext import ndb


class Project(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    folder = ndb.StringProperty()
    owner = ndb.StringProperty()
    # possible values A(Archived) IP (In Progress) F (Finished)
    status = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now_add=True)
    last_updated = ndb.DateTimeProperty(auto_now=True)


class ProjectTasks(ndb.Model):
    name = ndb.StringProperty()
    summary = ndb.StringProperty()
    estimated_hours = ndb.IntegerProperty()
    estimated_start = ndb.DateProperty()
    estimated_completion = ndb.DateProperty()
    status = ndb.StringProperty()
    project_key = ndb.IntegerProperty()
    created_on = ndb.DateTimeProperty(auto_now_add=True)
    last_updated = ndb.DateTimeProperty(auto_now=True)

