from firestone.handlers import ModelHandler, BaseHandler
from firestone.authentication import SessionAuthentication
from django.contrib.auth.models import User
from django.http import HttpResponse

# TODO: Add more models, with FK to the User model.
# Examine outputs of handler if they are correct.
# Then try BaseHandlers 
# Then, use request level field selection
# Then, use JSON serializer.
# Then, examine dispatch() and how I can decoraete it to do stuff before and
# after the request action is executed.

class DataHandler(BaseHandler):

    user_template = {
        'fields': ['id', 'username', 'email']
    }        
    template = {
        'fields': ['dic', 'list', 'user'],
        'related': {
            'user': user_template    
        }
    }

class UserHandlerSessionAuth(ModelHandler):
    model = User
    http_methods = ['get', 'delete']
    authentication = SessionAuthentication
    filters = ('filter_id', 'filter_name',)

    # TODO: IF I only expose 1 field of content_type, instead of getting it as
    # 'content_type': {key:value}, I get it as 'content_type': value.
    # Is there an option to disable this? Does the same happen with all
    # templates, at any depth, or have i simply hit a depth limit or sth?
    # Update: Had to use `flat`
    content_type_template = {
        'fields': ['id', ],
        'flat': False,
    }            
    logentry_template = {
        'fields': ['action_flag', 'content_type'],     
        'related': {
            'content_type': content_type_template,
        }
    }
    template = {
        'fields': ['id', 'username', 'first_name', 'last_name',
                   'logentry_set', 'email', 'last_login'], 
        'related': {
            'logentry_set': logentry_template,
        }, 
        'exclude': ['password', 'date_joined',],
        'allow_missing': True,
    }            

    def filter_id(self, data, request, *args, **kwargs):
        ids = request.GET.getlist('id')
        if ids:
            data = User.objects.filter(id__in=ids)            
        return data            

    def filter_name(self, data, request, *args, **kwargs):
        names = request.GET.getlist('name')
        if names:
            data = data.filter(first_name__in=names)
        return data
                    

class UserHandlerNoAuth(ModelHandler):
    model = User
    http_methods = ['GET']

    template = UserHandlerSessionAuth.template

    def get(self, request, *args, **kwargs):
        return

