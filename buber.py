"""
Filename: buber.py

### Description: ###
An application to provide information on specific bus numbers
through Colchester, Essex, UK

This will be done with the help of the transportapi
https://developer.transportapi.com/

Map plotting is via folium and the following tutorial
https://www.geeksforgeeks.org/python-plotting-google-map-using-folium-package/?ref=rp

### Basic Decomposition: - "Eat the elephant one bite at a time" ###
1. Hide API key and Program ID so we dont need to keep entering it or URLS - Done
2. Retreive data for the Number 65 bus heading outbound - Done
3. Take user input for bus number. Only allow then to enter the buses we have supplied - Done
    3.1 If user enter an incorrect bus number twice offer them the option to find the bus number by final destination
        - NEEDS IMPLEMENTING
4. User enters a bus number. We are only using a subset of buses for Colchester. "64", "65", "67", "70", "74", "88",
   "104".
   We have atcocodes for these stops and can define start and end points
5. User enters a destination - Program tells user what bus goes there and when the next departure is (from Town Center)
6. Display data to user on a map. - Milestone 1 - Done

### Questions the app should be able to answer ###
1. When is the next bus - enter bus number return next bus time.
2. Given a location display what buses go there. if you select a bus then display the time of the next bus.

### Future work if we have time ###
1. Make a windows graphical app
2. Make an android graphical app
3. Deploy it to a virtual android phone and run it

TRANSPORT API - app_id & app_key are not a valid keys in the examples below. Yoou need to reg as a developer at
transportapi.com to generate your own API key

1. This URL identifies One particular bus service, identified by line and operator - Function bus_service(bus_number)
It can be used to get the BUS_START and BUS_END of the journey
RETURNS: bus_number, outbound, inbound

'https://transportapi.com/v3/uk/bus/services/FESX:65.json?app_id=8e1c41c&app_key=ebaa5b9461f7f42778146f909073d17a'

2. Bus departures at a given bus stop (live) - Function next_bus_live()
By passing in the atcocode for the bus stop you can get live departure information for that stop
##PARAMETERS TO PROVIDE
atcocode

##INTERESTING VALUES IN RETURENED DATA
line_name, direction, status, best_departure_estimate

This returns any bus operating company utilising that stop
Data is returned in a dictionary of x lists where x is the number of buses that use that stop

First part of data recieved from url pull

{'65': [{'mode': 'bus', 'line': '65', 'line_name': '65', 'direction': 'Highwoods Tesco', 'operator': 'FESX',
'date': '2020-05-19', 'expected_departure_date': '2020-05-19', 'aimed_departure_time': '09:32',
'expected_departure_time': '09:30', 'best_departure_estimate': '09:30',
'status': {'cancellation': {'value': False, 'reason': None}}, 'source': 'FirstTicketerNationwide', 'dir': 'outbound',
'operator_name': 'First Essex',
'id': <URL>>

'https://transportapi.com/v3/uk/bus/stop/1500AA20/live.json?app_id=8e1c41c& \
app_key=ebaa5b9461f7f42778146f909073d17a&group=route&nextbuses=yes'

3. Bus departures at a given bus stop (timetabled) - Function next_bus_timetabled()
This URL gives you the timetabled information for that particulatr stop
##PARAMETERS TO PROVIDE
date, time, atcocode

https://transportapi.com/v3/uk/bus/stop/1500AA20/2020-05-15/07:10/timetable.json?app_id=8e1c41c& \
app_key=ebaa5b9461f7f42778146f909073d17a&group=route

4. The route of one specific bus - Function bus_route()
This gives every stop the bus will make between its atcocode bust stop and the final destination

##PARAMETERS TO PROVIDE
date, time, atcocode

https://transportapi.com/v3/uk/bus/route/FESX/65/outbound/1500AA20/2020-05-15/07:10/timetable.json?app_id=8e1c41c& \
app_key=ebaa5b9461f7f42778146f909073d17a&edge_geometry=false&stops=ALL
"""

# Import Libraries we need
import urllib3
import json
import pandas as pd
import requests
import folium
import sys
import os
import webbrowser
import logging
import time
from datetime import date


# Import our buberconfig
import buberconfig

# Set up logging - Default id to ,log info and above
# change 'level=logging.INFO' to 'level=logging.DEBUG' to get debug messages
logging.basicConfig(filename='log/buber.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Uncomment the logging.disable line to disable logging.
# Setting it to logging.CRITICAL disabled all logging
# CRITICAL and below Logging levels in order lowest to
# highest are as follows
# DEBUG (Lowest, INFO, WARNING, ERROR, CRITICAL (Highest)
#logging.disable(logging.CRITICAL)

# Start logging Program
logging.info('Start of Program')

# Constants
BASE_URL = 'https://transportapi.com/v3/uk/bus'
TODAY = date.today()
# define day of week for Sunday (0 - Monday, 1 - Tuesday, 2 - Wednesday, 3 - Thursday, 4 - Friday, 5 - Satarday,
# 6 - Sunday) - Get this from datetime - datetime.date.today().weekday() - Gives numeric for day of week
SUNDAY = 6
starttime = time.time()

def main():

    # Ask the user to input a bus number
    what_bus = input("Which First Essex bus do you require?: ")

    # Validate if it is a service we support
    bus = validate_bus(what_bus)

    # Get the bus Route
    bus_route(bus)

    # only work on valid bus routes supported by our application
    if bus != "Unsupported service":
        # Get some information on the bus_service
        bus_serv, outbound, inbound = bus_service(bus)
        print("Bus Number: " + bus_serv + " , Travels between " + outbound + ", and " + inbound)
        print("Preparing route map for the number " + bus_serv + " bus." )
        print("This will only take a short while...")
    else:
        logging.debug('DEBUG 0: Unsupported bus %s. Program exits via sys.exit' % what_bus)
        logging.info('End of Program')
        sys.exit("Unsupported service at this time. Goodbye")

def validate_bus(what_bus):
    """
    Validate if the bus service number is supported by our application.

    Args:
        what_bus (str): The bus service number to validate.

    Returns:
        str: The validated bus service number if it is supported by our application.
            Otherwise, a message indicating that the service is unsupported.

    """
    try:
        # These are only First Essex buses
        buses = {"S4", "65", "67", "70", "74B", "88", "104"}

        if what_bus in buses:
            return what_bus
        else:
            raise ValueError(f"We do not support bus service number {what_bus} at this time. Supported buses are: {', '.join(buses)}")
    except ValueError as e:
        return str(e)

def bus_service(bus_number):
    """
    Retrieve the endpoints of a bus service given its number.

    Args:
        bus_number (str): The number of the bus service to retrieve.

    Returns:
        tuple: A tuple containing the bus service number and its endpoints.

    Raises:
        ValueError: If the bus service number is invalid or cannot be retrieved.

    """
    try:
        bus_num = bus_number

        # Retrieve a URL via requests
        # Use f-strings to pass in the Constants and Variables to make up the URL
        url = f"{BASE_URL}/services/FESX:{bus_num}.json?app_id={buberconfig.APP_ID}&app_key={buberconfig.API_KEY}"

        response = requests.get(url)
        response.raise_for_status()

        bus_service_dict = response.json()
        outbound = bus_service_dict['directions'][0]['destination']['description']
        inbound = bus_service_dict['directions'][1]['destination']['description']

        # Return the bus number and its endpoints
        return bus_num, outbound, inbound
    except (requests.exceptions.RequestException, ValueError) as e:
        raise ValueError(f"Failed to retrieve bus service {bus_number}: {e}")

def next_bus_live():
    """
    Retrieve live data for the next buses at a specific stop.

    Returns:
        dict: A dictionary containing the live data for the next buses at the specified stop.

    Raises:
        ValueError: If the live data cannot be retrieved.

    """
    try:
        # Retrieve a URL via requests
        # Use f-strings to pass in the Constants and Variables to make up the URL
        url = f"{BASE_URL}/stop/1500AA20/live.json?app_id={buberconfig.APP_ID}&app_key={buberconfig.API_KEY}&group=route&nextbuses=yes"

        response = requests.get(url)
        response.raise_for_status()

        next_bus_live_dict = response.json()
        print(next_bus_live_dict)
        return next_bus_live_dict
    except (requests.exceptions.RequestException, ValueError) as e:
        raise ValueError(f"Failed to retrieve live bus data: {e}")

def next_bus_timetabled():
    """
    Retrieve timetabled data for the next buses at a specific stop.

    Returns:
        dict: A dictionary containing the timetabled data for the next buses at the specified stop.

    Raises:
        ValueError: If the timetabled data cannot be retrieved.

    """
    try:
        # Retrieve a URL via requests
        # Use f-strings to pass in the Constants and Variables to make up the URL
        url = f"{BASE_URL}/stop/1500AA20/{TODAY}/07:10/timetable.json?app_id={buberconfig.APP_ID}&app_key={buberconfig.API_KEY}"

        response = requests.get(url)
        response.raise_for_status()

        next_bus_timetabled_dict = response.json()
        #print(next_bus_timetabled_dict)
        return next_bus_timetabled_dict
    except (requests.exceptions.RequestException, ValueError) as e:
        raise ValueError(f"Failed to retrieve timetabled bus data: {e}")

def bus_route(bus_number):
    """
    Retrieve route data for a specific bus service number.

    Args:
        bus_number (str): The number of the bus service to retrieve.

    Returns:
        list: A list containing the bus stand, latitude, and longitude of each stop along the bus route.

    Raises:
        ValueError: If the route data cannot be retrieved.

    """
    try:
        bus = bus_number

        # Retrieve a URL via requests
        # Use f-strings to pass in the Constants and Variables to make up the URL
        if bus == "64":
            url = f"{BASE_URL}/route/FESX/{bus}/inbound/1500IM140/{TODAY}/07:05/timetable.json?app_id={buberconfig.APP_ID}&app_key={buberconfig.API_KEY}&edge_geometry=false&stops=ALL"
        elif bus == "65":
            url = f"{BASE_URL}/route/FESX/{bus}/inbound/1500IM2456B/{TODAY}/19:27/timetable.json?app_id={buberconfig.APP_ID}&app_key={buberconfig.API_KEY}&edge_geometry=false&stops=ALL"
        elif bus == "67":
            url = f"{BASE_URL}/route/FESX/{bus}/inbound/150033038003/{TODAY}/06:55/timetable.json?app_id={buberconfig.APP_ID}&app_key={buberconfig.API_KEY}&edge_geometry=false&stops=ALL"
        elif bus == "70":
            url = f"{BASE_URL}/route/FESX/{bus}/inbound/1500IM77A/{TODAY}/06:51/timetable.json?app_id={buberconfig.APP_ID}&app_key={buberconfig.API_KEY}&edge_geometry=false&stops=ALL"
        elif bus == "74B":
            url = f"{BASE_URL}/route/FESX/{bus}/inbound/15003303800B/{TODAY}/20:10/timetable.json?app_id={buberconfig.APP_ID}&app_key={buberconfig.API_KEY}&edge_geometry=false&stops=ALL"
        elif bus == "88":
            url = f"{BASE_URL}/route/FESX/{bus}/inbound/1500IM77A/{TODAY}/05:50/timetable.json?app_id={buberconfig.APP_ID}&app_key={buberconfig.API_KEY}&edge_geometry=false&stops=ALL"
        else:   # The 104
            url = f"{BASE_URL}/route/FESX/{bus}/inbound/1500IM52/{TODAY}/06:00/timetable.json?app_id={buberconfig.APP_ID}&app_key={buberconfig.API_KEY}&edge_geometry=false&stops=ALL"

        response = requests.get(url)
        response.raise_for_status()

        bus_route_dict = response.json()

        # Create a list of bus stands, latitudes, and longitudes
        bus_route_list = [[stop['stop_name'], stop['latitude'], stop['longitude']] for stop in bus_route_dict['stops']]

        logging.debug('DEBUG 5: Bus Route List ' + str(bus_route_list))

        return bus_route_list
    except (requests.exceptions.RequestException, ValueError) as e:
        raise ValueError(f"Failed to retrieve bus route data for bus service {bus_number}: {e}")


def map_it(bus_route_list):
    """
    Map the bus route on a Folium map.

    Args:
        bus_route_list (list): A list containing the bus stand, latitude, and longitude of each stop along the bus route.

    Raises:
        ValueError: If the map cannot be created.

    """
    try:
        # Convert the list to a pandas DataFrame
        map_it_df = pd.DataFrame(bus_route_list)

        # Rename the DataFrame columns
        map_it_df.columns = ['stop', 'lat', 'long']
        logging.debug('DEBUG 6: map_it_df.head()' + str(map_it_df.head()))

        # Prepare the data for the map
        locations = map_it_df[['lat', 'long']]
        locationlist = locations.values.tolist()

        # Build the map centered on Colchester, Essex
        route_map = folium.Map(location=[51.8959, 0.8919], zoom_start=14)

        # Plot the stops on the map and add their names as popups
        for point in range(0, len(locationlist)):
            folium.Marker((locationlist[point]), popup=map_it_df['stop'][point]).add_to(route_map)

        # Save the map to a file and open it in the browser
        route_map.save("c:\\Data\\PythonProjects\\buber\\route_maps\\route_map.html ")
        webbrowser.open('file://' + os.path.realpath('c:\\Data\\PythonProjects\\buber\\route_maps\\route_map.html'))
    except Exception as e:
        raise ValueError(f"Failed to create bus route map: {e}")

if __name__ == '__main__':
    main()

# Record how long the program took to run and then stop logging program
logging.info('Program Run Time (s): ' + str(time.time() - starttime))
logging.info('End of Program')

