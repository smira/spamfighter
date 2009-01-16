"""
Requires simplejson; can be downloaded from 
http://cheeseshop.python.org/pypi/simplejson
"""
import xmlrpclib

try:
    import json as simplejson
except ImportError:
    import simplejson

# From xmlrpclib
SERVER_ERROR          = xmlrpclib.SERVER_ERROR
NOT_WELLFORMED_ERROR  = xmlrpclib.NOT_WELLFORMED_ERROR
UNSUPPORTED_ENCODING  = xmlrpclib.UNSUPPORTED_ENCODING
INVALID_ENCODING_CHAR = xmlrpclib.INVALID_ENCODING_CHAR
INVALID_JSONRPC       = xmlrpclib.INVALID_XMLRPC
METHOD_NOT_FOUND      = xmlrpclib.METHOD_NOT_FOUND
INVALID_METHOD_PARAMS = xmlrpclib.INVALID_METHOD_PARAMS
INTERNAL_ERROR        = xmlrpclib.INTERNAL_ERROR
# Custom errors
METHOD_NOT_CALLABLE   = -32604

class Fault(xmlrpclib.Fault):
    def __init__(self, *args, **kwargs):
        self.requestId = kwargs.pop('requestId', None)
        xmlrpclib.Fault.__init__(self, *args, **kwargs)
    

class NoSuchFunction(Fault):
    """
    There is no function by the given name.
    """

def dumps(obj, **kws):
    requestId = kws.pop('requestId', None)
    if isinstance(obj, Exception):
        value = { 'error' : {'origin': obj.__class__.__name__,
            'code': obj.faultCode,
            'message': obj.faultString }}
        if isinstance(obj, Fault) and obj.requestId is not None:
            value['id'] = obj.requestId
        obj = value
    else:
        obj = { 'result' : obj }
        if requestId is not None:
            obj['id'] = requestId
    return simplejson.dumps(obj, **kws)

def loads(string, **kws):
    unmarshalled = simplejson.loads(string, **kws)
    if (isinstance(unmarshalled, dict) and
        unmarshalled.has_key('error')):
        raise Fault(unmarshalled['error']['code'],
            unmarshalled['error']['message'])
    if isinstance(unmarshalled, dict) and unmarshalled.has_key('result'):
        return unmarshalled['result']
    return unmarshalled

class SimpleParser(object):

    def feed(self, data):
        self.data = loads(data)

    def close(self):
        pass

class SimpleUnmarshaller(object):

    def getmethodname(self):
        return self.parser.data.get("method")

    def close(self):
        if isinstance(self.parser.data, dict):
            return self.parser.data.get("params")
        return self.parser.data

def getparser():
    parser = SimpleParser()
    marshaller = SimpleUnmarshaller()
    marshaller.parser = parser
    return parser, marshaller

class Transport(xmlrpclib.Transport):
    """
    Handles an HTTP transaction to an XML-RPC server.
    """
    user_agent = "jsonrpclib.py (by txJSON-RPC)"

    def getparser(self):
        """
        Get Parser and unmarshaller.
        """
        return getparser()

class ServerProxy(xmlrpclib.ServerProxy):
    """

    """
    def __init__(self, uri, transport=Transport(), *args, **kwds):
        xmlrpclib.ServerProxy.__init__(self, uri, transport, *args, **kwds)

    def __request(self, method, args):
        """
        Call a method on the remote server.
        """
        request = dumps({'method':method, 'params':args})
        response = self.__transport.request(
            self.__host,
            self.__handler,
            request,
            verbose=self.__verbose
            )
        if len(response) == 1:
            response = response[0]
        return response

