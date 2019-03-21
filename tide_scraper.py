import httplib2
from bs4 import BeautifulSoup, SoupStrainer

http = httplib2.Http()
status, response = http.request('https://tidesandcurrents.noaa.gov/stations.html')


def get_regions():
    soup = BeautifulSoup(response, 'html.parser')
    regions = soup.findAll("span", attrs={'class': None})
    regions.remove(regions[len(regions) - 1])
    return regions


def get_stations_dict():
    soup = BeautifulSoup(response, 'html.parser')
    stations_dict = dict()
    regions = soup.findAll("div", attrs={'class': 'span12 areaheader'})
    keys = []
    temp = [] 

    for region in regions:
        keys.append(region.get('id'))
    for key in keys:
        stations_dict[key] = []
    for key in stations_dict:
        temp = list()
        for region in regions:
            if key in region.get('id'):
                sub_regions = region.findAll("div", attrs={'class': lambda l: l and l.startswith('span4')})
                for sub_region in sub_regions:
                    value = "%s" % sub_region.find('a').text
                    temp.append(value)
            stations_dict[key] = temp
    return stations_dict


# Might want to consider implementing this cleaner approach
def get_station_by_region(region):
    stations_dict = get_stations_dict()
    local_stations = stations_dict.get(region)
    print(local_stations)
    return local_stations
