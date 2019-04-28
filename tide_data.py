from datetime import datetime
import time
import re


def split_times_to_datetimes(split_times):
    results = []
    current_time = datetime.today()
    for tide in split_times:
        test_time = str(current_time.year) + " " + str(current_time.month) + " " + str(current_time.day) + " " + str(
            tide[0]) + str(tide[1])
        date_object = datetime.strptime(test_time, '%Y %m %d %I:%M %p')
        results.append([date_object, tide[2].split(' ')[0]])

    return results


def get_data_points(current_time, tide_times):
    results = []
    last_item = None
    # Compare current time with tide times
    for tide in tide_times:
        if tide[0] < current_time:
            last_item = tide[0]
        else:
            prev_time = last_item
            next_time = tide[0]
            results.extend([prev_time, current_time, next_time])
    return results


def get_light_intensity(data_points):
    # Get fraction of tide
    # light_intensity = time.mktime(data_points[0][0].timetuple())
    prev_time = data_points[0]
    current_time = data_points[1]
    next_time = data_points[2]

    prev_time_seconds = float(time.mktime(prev_time.timetuple()))
    current_time_seconds = float(time.mktime(current_time.timetuple()))
    next_time_seconds = float(time.mktime(next_time.timetuple()))

    numerator = (next_time_seconds - prev_time_seconds) / 10
    denomenator = current_time_seconds - prev_time_seconds
    light_intensity = (numerator / denomenator) * 100

    return light_intensity

def split_tide_string(times):
    # Split the tide time data 
    # Example: [' 1:48  AM ', 'low', ' 0.71 ft.']
    tide_string = []
    for data in times:
        tide_regex = re.split('(low|high)', data)
        tide_string.append(tide_regex)
    return tide_string