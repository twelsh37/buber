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
1. Hold API key and Program ID so we dont need to keep entering it or URLS
2. Retreive data for the Number 65 bus heading outbound
3. Take user input for bus number. Only allow then to enter the buses we have supplied
    3.1 If user enter an incorrect bus number twice offer them the option to find the bus number by final destination
4. User enters a bus number. We are only using a subset of buses for Colchester. "64", "65", "67", "70", "74", "88",
   "104".
   We have atcocodes for these stops and can define start and end points
5. User enters a destination - Program tells user what bus goes there and when the next departure is (from Town Center)
6. Display data to user on a map. - Milestone 1

### Questions the app should be able to answer ###
1. When is the next bus - enter bus number return next bus time for town center location
2. Given a location display what busses go there. if you select a bus then display the time of the next bus

### Future work if we have time ###
1. Make a windows graphical app
2. Make an android graphical app
3. Deploy ity to a virtual android phone and run it

Tools/Frameworks
1. Kivy Framework - https://realpython.com/mobile-app-kivy-python/
2. Android dev app - https://developer.android.com/studio

TRANSPORT API
1. This URL identifies One particular bus service, identified by line and operator - Function bus_service(bus_number)
It can be used to get the BUS_START and BUS_END of the journey
RETURNS: bus_number, outbound, inbound

'https://transportapi.com/v3/uk/bus/services/FESX:65.json?app_id=9e91c41c&app_key=ebaa5b9461f7f42778146f909073d17a'


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

'https://transportapi.com/v3/uk/bus/stop/1500AA20/live.json?app_id=9e91c41c& \
app_key=ebaa5b9461f7f42778146f909073d17a&group=route&nextbuses=yes'

3. Bus departures at a given bus stop (timetabled) - Function next_bus_timetabled()
This URL gives you the timetabled information for that particulatr stop
##PARAMETERS TO PROVIDE
date, time, atcocode

https://transportapi.com/v3/uk/bus/stop/1500AA20/2020-05-15/07:10/timetable.json?app_id=9e91c41c& \
app_key=ebaa5b9461f7f42778146f909073d17a&group=route

4. The route of one specific bus - Function bus_route()
This gives every stop the bus will make between its atcocode bust stop and the final destination

##PARAMETERS TO PROVIDE
date, time, atcocode

https://transportapi.com/v3/uk/bus/route/FESX/65/outbound/1500AA20/2020-05-15/07:10/timetable.json?app_id=9e91c41c& \
app_key=ebaa5b9461f7f42778146f909073d17a&edge_geometry=false&stops=ALL

"""
# Import Libraries we need
import urllib3
import json
import pandas as pd
import folium
import sys
import os
import webbrowser
import logging
from datetime import date

# Import our buberconfig
import buberconfig

# Set up logging
logging.basicConfig(filename='log/buber.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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


def main():
    # Ask the user to input a bus number
    what_bus = input("Which First Essex bus do you require?: ")

    # Validate if it is a service we support
    bus = validate_bus(what_bus)

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

        # We dont actually use stop, lat and l,ong here, we just pass
        # the bus to the bus_route function.


def validate_bus(what_bus):
    # Function to validate we have a valid bus for our application
    # Evaluate the user input
    # Is the users bus selection in our buses list? if yes, then procced
    # These are only First Essex buses
    buses = ["64", "65", "67", "70", "74B", "88", "104"]

    if what_bus in buses:
        return what_bus
    else:
        print("We do not support bus service number " + str(what_bus) + " at this time")
        print("supported buses are: " + str(buses)[1:-1])
        return "Unsupported service"

def bus_service(bus_number):

    bus_num = bus_number

    # Retrieve a URL via urllib3
    # Use %s to pass in the Constants and Variables to make up the URL
    url = BASE_URL + '/services/FESX:%s.json?app_id=%s&app_key=%s' % (bus_num, buberconfig.APP_ID, buberconfig.API_KEY)
    logging.debug('DEBUG 2: APP_ID: ' + buberconfig.APP_ID + ' API_KEY:  '+ buberconfig.API_KEY)

    http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    response = http.request('GET', url)
    bus_service_dict = json.loads(response.data.decode('utf-8'))
    outbound = bus_service_dict['directions'][0]['destination']['description']
    inbound = bus_service_dict['directions'][1]['destination']['description']

    # Return the bus number and its endpoints
    return bus_num, outbound, inbound

def next_bus_live():
    # URL to retrieve data. This may need more paramaters to be passed in. Currently only APP_ID and API_KEY
    url = BASE_URL + '/stop/1500AA20/live.json?app_id=buberconfig.APP_ID&app_key=buberconfig.API_KEY&group=route&' \
                     'nextbuses=yes'

    http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    response = http.request('GET', url)
    next_bus_live_dict = json.loads(response.data.decode('utf-8'))
    print(next_bus_live_dict)

def next_bus_timetabled():
    # URL to retrieve data. This may need more paramaters to be passed in. Currently only APP_ID and API_KEY
    url = BASE_URL + '/stop/1500AA20/%s/07:10/timetable.json?app_id=buberconfig.APP_ID&' \
                     'app_key=buberconfig.API_KEY' % (TODAY)

    http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    response = http.request('GET', url)
    next_bus_timetabled_dict = json.loads(response.data.decode('utf-8'))
    print(next_bus_timetabled_dict)

def bus_route(bus_number):
    # This function queries the transport API for route data for a specific bus service number
    # It receives input as bus_number from main()
    # it provides bus_stand, lat and long of each of the stops along the specific buses route
    # and passes them to map_it() for route mapping.

    bus = bus_number
    # Retrieve a URL via urllib3
    # This could be tidied up using data from URL but for expediancy it is coded in here
    # Use %s to pass in the Constants and Variables to make up the URL
    if bus == "64":
        url = BASE_URL + '/route/FESX/%s/inbound/1500IM2349B/%s/06:40/timetable.json?app_id=buberconfig.APP_ID'\
                         '&app_key=buberconfig.API_KEY&edge_geometry=false&stops=ALL' % (bus, TODAY)
    elif bus == "65":
        url = BASE_URL + '/route/FESX/%s/inbound/1500IM2456B/%s/19:27/timetable.json?app_id=buberconfig.APP_ID'\
                         '&app_key=buberconfig.API_KEY&edge_geometry=false&stops=ALL' % (bus, TODAY)
    elif bus == "67":
        url = BASE_URL + '/route/FESX/%s/inbound/150033038003/%s/06:55/timetable.json?' \
                         'app_id=buberconfig.APP_ID&app_key=buberconfig.API_KEY&edge_geometry=false&stops=ALL' % (bus, TODAY)
    elif bus == "70":
        url = BASE_URL + '/route/FESX/%s/inbound/1500IM77A/%s/06:51/timetable.json?app_id=buberconfig.APP_ID' \
                         '&app_key=buberconfig.API_KEY&edge_geometry=false&stops=ALL' % (bus, TODAY)
    elif bus == "74B":
        url = BASE_URL + '/route/FESX/%s/inbound/15003303800B/%s/20:10/timetable.json?' \
                         'app_id=buberconfig.APP_ID&app_key=buberconfig.API_KEY&edge_geometry=false&stops=ALL' % (bus, TODAY)
    elif bus == "88":
        url = BASE_URL + '/route/FESX/%s/inbound/1500IM77A/%s/05:50/timetable.json?app_id=buberconfig.APP_ID&' \
                        'app_key=buberconfig.API_KEY&edge_geometry=false&stops=ALL' % (bus, TODAY)
    else:   # The 104
        url = BASE_URL + '/route/FESX/%s/inbound/1500IM52/%s/06:00/timetable.json?app_id=buberconfig.APP_ID&' \
                         'app_key=buberconfig.API_KEY&edge_geometry=false&stops=ALL' % (bus, TODAY)

    http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    response = http.request('GET', url)
    bus_route_dict = json.loads(response.data.decode('utf-8'))

    # Create a blank list that will be passed to Map_it() function
    bus_route_list = []

    # iterate through our dictionary giving us the bus stop names and their
    # lat and long so we can plot them on a map.
    for stop in bus_route_dict['stops']:
        bus_stand = stop['stop_name']
        lat = stop['latitude']
        long = stop['longitude']
        bus_route_list.append([bus_stand,lat,long])

    #map_it(bus_route_list)
    return bus_route_list

def map_it(bus_route_list):
    # This function maps teh bus route on a folium map
    # It receives input as bus_stand, lat, and long from bus_route

    # lets get the list into pandas
    map_it_df = pd.DataFrame(bus_route_list)

    # Rename the Dataframe column headings
    # to something more meaningful
    map_it_df.columns=['stop', 'lat', 'long']
    print(map_it_df.head())

    # Prep data for the map
    locations = map_it_df[['lat', 'long']]
    locationlist = locations.values.tolist()

    # Now build the map centered on Colchester Essex
    route_map = folium.Map(location=[51.8959,0.8919] , zoom_start=14)

    # Run through the list of stops and plot them on a map.
    # add Bus Stop names to the markers
    # Finally save teh route_map so it can be displayed later
    for point in range(0, len(locationlist)):
        folium.Marker((locationlist[point]) , popup=map_it_df['stop'][point]).add_to(route_map)
        route_map.save("route_maps/route_map.html ")

    # open the route map in our browser
    webbrowser.open('file://' + os.path.realpath('C:/Data/Stanford/code/buber/route_maps/route_map.html'))

if __name__ == '__main__':
    main()

# Stop logging Program
logging.info('End of Program')