from entity import *

CHARTS = {
'fans adds last day':           'bb789492225c4c4da2e15f617acc9982',
'fans adds last week':          'a5e7dbdfcd984dc28c350c26a2e703c0',
'fans daily high flyers':       'c6db7136d639444d9ab54a3c66e0b813',
'fans total':                   '6aacf495049d4de99c809b0ad8120c39',
'video views last day':         '1574c43703344292a753fecf0f793c2e',
'video views last week':        'b0de4888427d46ac8f599f2f6d51e293',
'video views total':            '3040cc0f02ed4dd1a2da9ea95c9a8272',
'new comments last day':        'd21e3cd170924bcd8874ec15d84b64f1',
'new comments last week':       '75f972a32f3547e197668d545f4cda1d',
'comments total':               '7908e358427f4efe9f5aac6df69bfcbd',
'plays last day':               'd527eeba4bdc42178b49d977b375936f',
'plays last week':              '627b42c981d4413b83191efd8183a982',
'plays daily high flyers':      'b857276b34cf488f9a934765c3281af7',
'plays total':                  '7a614a370a2848b29c156e27dde582c8',
'page views last day':          '8a826f01468d43d7b64d829d5f889e04',
'page views last week':         '3fc5101590484f15ae48903ec6ce3ed5',
'page views daily high flyers': '8f55159307d6429fac6c5e9b04fc6449',
'page views total':             '765855505c7f4e3bb1fc887740f2dd1a',
'downloads daily high flyers':  '2960402fc260409c8bcd75b00d8dc4c8'
}

class Chart(Entity):
    """
    wraps the chart entity type as described at http://developer.musicmetric.com/charts.html
    self.[chart_entity_type] is a generator of the objects in the chart, eg for a chart of artists
    self.artist is a generator of tuples of the form (rank, value, artist class instances)
    """
    def __init__(self, chartUUID):
        self.entity_type = 'chart'
        if chartUUID in CHARTS:
            self.entity_id = CHARTS[chartUUID]
        elif len(chartUUID) == 32:
            self.entity_id = chartUUID
        else:
            raise ValueError("Unknown chart type")
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
        
