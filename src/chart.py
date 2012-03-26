from entity import *


class Chart(Entity):
    """
    wraps the chart entity type as described at http://developer.musicmetric.com/charts.html
    self.[chart_entity_type] is a generator of the objects in the chart, eg for a chart of artists
    self.artist is a generator of tuples of the form (rank, value, artist class instances)
    """
    def __init__(self, chartUUID):
        self.entity_type = 'chart'
        self.entity_id = chartUUID
        self.response_from()
        assert self.response['class'] == "chart" #verify that uuid is a chart
        chart_type = [e_type
                      for e_type in self.response['data'][0].keys()
                         if not e_type in ("rank","value")][0]
        #import the correct chart type, module will be all lower, clase will be titled (eg. artist.Artist)
        mod = __import__('mmpy.'+chart_type.lower()) #will error if class is unsupported
        cls = getattr(mod, chart_type.title())
        
        setattr(self, chart_type.lower(),
                ((item["rank"], item["value"], cls(item[chart_type]['id'], name=item[chart_type]['name']))
                 for item in self.response['data']))
        for key, val in self.response.items():
            if key != "data":
                setattr(self, key, val)
        
