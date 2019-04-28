import httplib2
from bs4 import BeautifulSoup
from selenium import webdriver

http = httplib2.Http()
main = 'https://tidesandcurrents.noaa.gov/stations.html'
status, response = http.request(main)

# def get_tide_data(value):
#     times = list()
#     tide_http = httplib2.Http()
#     tide_data = value
#     tide_status, tide_response = tide_http.request(tide_data)
#     soup = BeautifulSoup(tide_response, 'html.parser')
#     table = soup.find("table", attrs={'class': 'table-condensed'}).findAll("tr", attrs={'class': None})
#     for tag in table:
#         times.append(tag.text)  

#     return times

def test(value):
    times = list()
    # tide_http = httplib2.Http()
    tide_data = value
    try:
        driver = webdriver.Chrome('./venv/bin/chromedriver')
        driver.get(value)           
        html = driver.page_source
    # tide_status, tide_response = tide_http.request(tide_data)
    except Exception as e:
        raise e
    finally:
        driver.close()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id='data_listing')
    for tag in table:
        times.append(tag.text)  
    return times

def get_regions():
    soup = BeautifulSoup(response, 'html.parser')
    regions = soup.findAll("span", attrs={'class': None})
    regions.remove(regions[len(regions) - 1])
    return regions


def get_water_level():
    soup = BeautifulSoup(response, 'html.parser')
    areas = soup.findAll("div", attrs={'class': 'span4'})
    return areas


def get_stations_dict():
    soup = BeautifulSoup(response, 'html.parser')
    stations_dict = dict()
    regions = soup.findAll("div", attrs={'class': 'span12 areaheader'})
    keys = []

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
