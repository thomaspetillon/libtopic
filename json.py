#!/usr/bin/env python
import traceback
from django.http import HttpResponse
from django.utils import simplejson
from django.db.models.query import QuerySet
from django.core.serializers import serialize

def json_response(function):
    """
    Decorator (@json_response) that encapsulates the result into a
    JsonResponse object and handle exceptions
    
    Nota : decorated function should accept one and only one argument : request
    """
    def _decorated_function(request):
        try:
            result = function(request)            
        except:
            result = [traceback.format_exc()]
        return JsonResponse(result)
    return _decorated_function

class JsonResponse(HttpResponse):
    def __init__(self, object):
        if isinstance(object, QuerySet):
            content = serialize('json', object)
        else:
            content = simplejson.dumps(object)
        super(JsonResponse, self).__init__(content, mimetype='application/json')        