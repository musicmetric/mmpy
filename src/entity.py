import logging
import os
import urllib2
from urllib import urlencode
import datetime
from simplejson import loads
from ConfigParser import SafeConfigParser, NoSectionError
from os.path import exists as pexists, join as pjoin, expanduser

#cascading config vars
config_path = pjoin(expanduser('~'), '.semetric')
cfg = SafeConfigParser()
try:
    BASE_URL = os.environ['BASE_URL']
except KeyError:
    try:
        cfg.read(pjoin(config_path, 'config'))
        BASE_URL = cfg.get('semetric','base.url')
    except:
        BASE_URL = "http://api.semetric.com/"

try:
    API_KEY = os.environ['SEMETRIC_KEY']
except KeyError:
    cfg.read(pjoin(config_path, 'config'))
    API_KEY = cfg.get('semetric','api.key')
except NoSectionError:
    API_KEY = None

log = logging.getLogger(__name__)

class Entity(object):
    """
    Base class for all entity types. Not intended to be directly instantiated
    """
    def __init__(self):
        """
        sets up the cache and sets entity_type and entity_id 
        """
        self.entity_type = None
        self.entity_id = None

    def __str__(self):
        id = getattr(self, 'id', self.entity_id)
        name = getattr(self, 'name', '<name unknown>')
        return "{0}::UUID - {1}:: Name - {2}".format(self.entity_type, id, name.encode('utf-8').replace('_',' '))
    
    def __eq__(self, other):
        if 'id' in self.__dict__ and 'id' in other.__dict__:
            # if fetched_summary on both, compare musicmetric IDs
            return self.id == other.id
        try:
            return self.entity_id == other.entity_id
        except AttributeError:
            #other doesn't have a defined entity_id, so they aren't equal
            return False
                                                                                    
    def _construct_timeseries(self, timeseries, constraints={}):
        """
        wraps response_from for timeseries calls, returns the resulting dict
        """
        self.response_from(timeseries, constraints)
        if self.response == None:
            return None
        return {'data':self.response['data'],
                'period':self.response['period'],
                'start time':datetime.datetime.fromtimestamp(self.response['start_time']),
                'end time':datetime.datetime.fromtimestamp(self.response['end_time'])}
        
    def response_from(self, ext_endpoint=None, params = {}):
        """
        fetches and parses data from the semetric API, returning whatever is
        in the 'response' field in the top level dict on success (200)
        if the endpoint returns a 204, returns None (no data available for id)
        else throws a value error
        self should have these attributes as needed:
        @entity_type the entity type (eg. list, artist)
        @entity_id the semetric UUID or resolvable equivelant for the entity to be retrieved
        these can be passed on call:
        @ext_endpoint (default: None) if an endpoint beyond the id is required, this is where it should go
        @params and key value params *besides* the api token
        on success self.response will have the contents of the response
        a 
        """
        params['token'] = API_KEY
        base_endpoint="{base_url}/{entity}/{entityID}"
        uri = base_endpoint.format(base_url=BASE_URL, entity=self.entity_type, entityID=self.entity_id)
        if ext_endpoint:
            if ext_endpoint[0] != '/':
                ext_endpoint = '/' + ext_endpoint
            uri += ext_endpoint
        full_uri = uri + '?' + urlencode(params)
        log.debug('fetching: {0}'.format(full_uri))
        wrapped_resp = loads(urllib2.urlopen(full_uri).read(), encoding='utf-8')
        #better error handling should go here
        if not wrapped_resp['success']:
            if wrapped_resp["error"]["code"] == 204:
                self.response = None
                return
            raise ValueError(\
                'Unable to fetch data for {0} entity with id {1}, ext_endpoint was {2}, params-{3}'.format(\
                    self.entity_type, self.entity_id, ext_endpoint, params)+
                ' code was {0}, msg {1}'.format(wrapped_resp["error"]["code"],wrapped_resp["error"]["msg"]))
        self.response = wrapped_resp["response"]
