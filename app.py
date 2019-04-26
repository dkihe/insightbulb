from flask import Flask, render_template, request
from yeelight import *
from tide_scraper import *
from tide_data import split_times_to_datetimes, get_data_points


from datetime import datetime
import threading

import httplib2
import re

app = Flask(__name__, static_url_path='/static')
app.config["TEMPLATES_AUTO_RELOAD"] = True
http = httplib2.Http()
current_times = list()
station_name = []


@app.route('/', methods=['GET', 'POST'])
def index():
    bulbs = discover_bulbs()
    devices = []

    weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    current_weekday = weekday[datetime.today().weekday()]
    current_date = str(datetime.today().month) + '/' + str(datetime.today().day)

    skip_regions = ['Great Lakes',
                    'Erie',
                    'Michigan',
                    'St. Clair',
                    'Niagara River',
                    'Lawrence',
                    'Caribbean',
                    'District of Columbia',
                    'Indian',
                    'New York',
                    'New Jersey',
                    'North Carolina',
                    'Pacific Islands',
                    'Portuguese Islands',
                    'Rhode Island',
                    'South Carolina']

    for bulb in bulbs:
        devices.append(bulb['capabilities'].get('id'))

    us_regions = [region.text for region in get_regions()]
    for skip in skip_regions:
        for region in us_regions:
            if skip in region:
                us_regions.remove(region)
    local_stations = get_stations_dict()

    # A tidal station was selected
    if request.method == 'POST':
        station_data = request.json['station_data']
        station_url = 'https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=%s' % station_data[0]
        times = get_tide_data(station_url)
        current_times.clear()
        extrema = tidal_flow(times)
        station_name.clear()
        station_name.append(station_data[1])
        # For debugging
        print("STATION_DATA:", station_data)
        for extreme in extrema:
            current_times.append(extreme)

    return render_template('index.html', us_regions=us_regions,
                           local_stations=local_stations, devices=devices,
                           current_weekday=current_weekday, current_date=current_date,
                           tide_times=current_times, station_name=station_name)


@app.route('/show-tide-extrema')
def update_tide_times():
    return render_template('index.html', tide_times=current_times)


@app.route('/get-stations')
def get_stations(region):
    local_stations = get_stations(region)
    return render_template('index.html', local_stations=local_stations)


# Turn the light on
@app.route('/turn-on')
def turn_on():
    bulbs = discover_bulbs()
    if len(bulbs) is 0:
        return render_template('index.html')
    my_bulb = Bulb(bulbs[0].get("ip"))
    my_bulb.turn_on(effect="sudden")
    return render_template('index.html')


# Turn the light off
@app.route('/turn-off')
def turn_off():
    bulbs = discover_bulbs()
    if len(bulbs) is 0:
        return render_template('index.html')
    my_bulb = Bulb(bulbs[0].get("ip"))
    my_bulb.turn_off(effect="sudden")
    return render_template('index.html')


def tidal_flow(times):
    bulbs = discover_bulbs()
    split_times = list()

    # split_times contains elements in the form:
    # ['2:51 ', 'AM', 'high 1.62 ft.']
    for tide in times:
        high_low = re.split('(low|high)', tide)
        split_times.append(high_low)

    if len(bulbs) is 0:
        return split_times

    # Notify when a station is selected
    my_bulb = Bulb(bulbs[0].get("ip"))
    station_select_pulse = [
        TemperatureTransition(1500, duration=500, brightness=50)]
    station_flow = Flow(
        count=2,
        transitions=station_select_pulse)
    my_bulb.start_flow(station_flow)

    # Apply the ambient alert notification using a delayed thread
    delayed_transitions = [
        TemperatureTransition(1700, duration=1000),
        SleepTransition(duration=1000),
        TemperatureTransition(6500, duration=1000),
        TemperatureTransition(500, 500)]
    delayed_alert_flow = Flow(
        count=2,
        action=Flow.actions.recover,
        transitions=delayed_transitions)

    # Get current time in seconds, data points (prev tide time, current time, next tide time)
    # Data points are converted to datetime objects
    # TODO: Implement the 'brightness-to-tide' feature with a thread that calls a
    #  function that runs a loop for as long as the known tidal change
    now = datetime.now()
    tidal_datetimes = split_times_to_datetimes(split_times)
    data_points = get_data_points(now, tidal_datetimes)
    if len(data_points) > 0:
        delay = (data_points.pop() - now).total_seconds()
        threading.Timer(delay, lambda: my_bulb.start_flow(delayed_alert_flow)).start()

    return split_times


if __name__ == '__main__':
    app.run(debug=True)
