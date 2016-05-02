import urllib2
from xml.etree import ElementTree
from aenum import Enum

class Services(Enum):
    TODAYS_RATES = 0
    ALL_RATES = 1

class RESTClient:
    namespaces = {
        'nsp': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'
    } 
    services_list = {
        Services.TODAYS_RATES: 'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml',
        Services.ALL_RATES: 'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.xml'
    }
    
    def __init__(self, service):
        if isinstance(service, Services):
            self.selected_service = service
        else:
            self.selected_service = None
            
        # TODO: load services links
        # services_list = ...
    
    def get_URL(self):
        # TODO: To be added to config file
        return self.services_list[self.selected_service]

    def decode_data(self, response):
        return ElementTree.ElementTree(ElementTree.fromstring(response))
    
    def organize_data(self, data):
        return data
    
    def call_service(self):
        url = self.get_URL()
        response = urllib2.urlopen(url).read()
        raw_data = self.decode_data(response)
        return self.organize_data(raw_data)