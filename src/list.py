from entity import *


class List(Entity):
    """
    wraps the list entity type as described at http://developer.musicmetric.com/lists.html
    """
    def __init__(self, listUUID):
        self.entity_type = 'list'
        self.entity_id = listUUID
        self.response_from()
        list_type = self.response['entities'][0]['class']#we assume a homogenious list
        setattr(self, list_type, self.response['entities'])
        
