import os
import mimetypes
from datetime import datetime

from django.http import HttpResponse
from django.utils.http import http_date
from django.utils import dateformat

from django.core.files.storage import default_storage as storage

def send_file(request, filepath, last_modified=None, filename=None):
    fullpath = filepath

    f = storage.open(fullpath)
    # Respect the If-Modified-Since header.
    if filename:
        mimetype, encoding = mimetypes.guess_type(filename)
    else:
        mimetype, encoding = mimetypes.guess_type(fullpath)
        
    mimetype = mimetype or 'application/octet-stream'
    response = HttpResponse(f.read(), mimetype=mimetype)
    
    if last_modified:
        if isinstance(last_modified, datetime):
            last_modified = float(dateformat.format(last_modified, 'U'))
        response["Last-Modified"] = http_date(epoch_seconds=last_modified)
    
    response["Content-Length"] = f.size
    
    if encoding:
        response["Content-Encoding"] = encoding
    
    # TODO: Escape filename
    if filename:
        response["Content-Disposition"] = "attachment; filename=%s" % filename.encode('utf-8')
    
    return response

