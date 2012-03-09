from entity import *


class Artist(Entity):
    """
    wraps the artist entity type as described at http://developer.musicmetric.com/timeseries.html
    """
    def __init__(self, artistUUID):
        self.entity_type = 'artist'
        self.entity_id = artistUUID
    def fetch_summary(self):
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

        
        
