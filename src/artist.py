from entity import *


class Artist(Entity):
    """
    wraps the artist entity type as described at http://developer.musicmetric.com/timeseries.html
    all timeseries are attributes of the form self.<type>_<source>, which sets a dict if there's data
    """
    summary_attrs = ("name", "id", "description", "previous_rank", "rank")
    def __init__(self, artistUUID, **kwargs):
        """
        creates an artist instance. UUID required(or equivelant 3rd party id with prefix,
        see http://developer.musicmetric.com/identification.html for details)
        any attributes that are in 
        """
        self.entity_type = 'artist'
        self.entity_id = artistUUID
        self.fetched_summary = False # prevent the summary from being fetched multiple times
        for key, val in kwargs.items():
            if key in Artist.summary_attrs:
                setattr(self, key, val)
            else:
                raise KeyError("unexpected creation attribute")

    def __str__(self):
        name = getattr(self, 'name', '<name unknown>')
        return "Artist::UUID - {0}:: Name - {1}".format(self.entity_id, name.encode('utf-8'))

    def __eq__(self, other):
        if 'id' in self.__dict__ and 'id' in other.__dict__:
            # if fetched_summary on both, compare musicmetric IDs
            return self.id == other.id
        try:
            return self.entity_id == other.entity_id
        except AttributeError:
            #other doesn't have a defined entity_id, so they aren't equal
            return False
    
    def __getattr__(self, attr):
        if attr in Artist.summary_attrs and not self.fetched_summary:
            self.fetch_summary()
            return getattr(self, attr)
        if len(attr.split('_')) == 2:
            try:
                result =  self._construct_timeseries(attr.replace('_', '/'))
                setattr(self, attr, result) # don't want to call the api over and over
                return result
            except ValueError:
                pass #call failed, probably not an endpoint
        raise AttributeError("Unknown attribute name: {0}".format(attr))
        # return getattr(super(Artist, self), attr)

    def fetch_summary(self):
        """
        grabs the summary info and sets the corisponding attributes.
        Note: overides existing attribute values for these attributes
        """
        self.response_from()
        #should really clean up the triple nest
        for k,v in self.response.items():
            if not isinstance(v,dict):
                setattr(self,k,v)
            else:
                for subk,subv in v.items():
                    if not isinstance(subv,dict):
                        setattr(self,subk,subv)
                    else:
                        for ssk,ssv in subv.items():
                            setattr(self,ssk,ssv)
        self.fetched_summary = True

        
        
