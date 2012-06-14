from entity import *


class Releasegroup(Entity):
    """
    wraps the ReleaseGroup entity type as described at http://developer.musicmetric.com
    all timeseries are attributes of the form self.<type>_<source>, which sets a dict if there's data
    """
    summary_attrs = ("name", "id", "description", "artist")
    def __init__(self, relgrpUUID, **kwargs):
        """
        creates a releasegroup instance. UUID required(or equivelant 3rd party id with prefix,
        see http://developer.musicmetric.com/identification.html for details)
        any attributes that are in 
        """
        self.entity_type = 'releasegroup'
        self.entity_id = relgrpUUID
        self.fetched_summary = False # prevent the summary from being fetched multiple times
        for key, val in kwargs.items():
            if key in Releasegroup.summary_attrs:
                setattr(self, key, val)
            else:
                raise KeyError("unexpected creation attribute")

    def __getattr__(self, attr):
        if attr in Releasegroup.summary_attrs and not self.fetched_summary:
            self.fetch_summary()
            return getattr(self, attr)
        if len(attr.split('_')) > 1:
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

        
        
