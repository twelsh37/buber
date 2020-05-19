"""
Filename: bus-locator.py

### Description: ###
An application to provide information onspecific bus numbers
through Colchester, Essex, UK

This will be done with the help of the transportapi
https://developer.transportapi.com/

Map plotting is via folium and teh following tutorial
https://www.geeksforgeeks.org/python-plotting-google-map-using-folium-package/?ref=rp

### Basic Decomposition: - "Eat the elephant one bite at a time" ###
1. Hold API key and Program ID so we dont need to keep entering it or URLS - DONE
2. Retreive data for the Number 65 bus heading outbound - DONE
3. Take user input for bus number. Only allow then to enter the busses we have supplied - DONE
    3.1 If user enter an incorrect bus number twice offer them the option to find the bus number by final destination
4. User enters a bus number - program tells user where bus comes and goes to and the departure time (from Town Center)
    4.1 Buses 62, 65, and 68 all return route data but that is because the URL being passed has the atcocode for
        Causton Road and these buses are on that route. Other routes will have different stops with different atcocodes.
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

'https://transportapi.com/v3/uk/bus/stop/1500AA20/live.json?app_id=9e91c41c&app_key=ebaa5b9461f7f42778146f909073d17a&group=route&nextbuses=yes'

3. Bus departures at a given bus stop (timetabled) - Function next_bus_timetabled()
This URL gives you the timetabled information for that particulatr stop
##PARAMETERS TO PROVIDE
date, time, atcocode

https://transportapi.com/v3/uk/bus/stop/1500AA20/2020-05-15/07:10/timetable.json?app_id=9e91c41c&app_key=ebaa5b9461f7f42778146f909073d17a&group=route

4. The route of one specific bus - Function bus_route()
This gives every stop the bus will make between its atcocode bust stop and the final destination

##PARAMETERS TO PROVIDE
date, time, atcocode

https://transportapi.com/v3/uk/bus/route/FESX/65/outbound/1500AA20/2020-05-15/07:10/timetable.json?app_id=9e91c41c&app_key=ebaa5b9461f7f42778146f909073d17a&edge_geometry=false&stops=ALL

"""
# Import Libraries we need
import urllib3
import json
import folium



# Constants
APP_ID = '9e91c41c'
API_KEY = 'ebaa5b9461f7f42778146f909073d17a'

def main():

    # variables for main
    fail_count = 0


    # Ask the user to input a bus number
    what_bus = input("What bus do you want?: ")

    # Evaluate the user input
    # Is the users bus selection in our busses list? if yes, then proced
    # These are only First Essex busses
    busses = ["17", "61", "62", "62A", "62B", "62C", "64", "64A", "65", "66", "66B", "67", "67B", "67C", "68", "70",
              "71", "71A", "71C", "71X", "74B", "75", "75A", "76", "88", "88A", "88B", "102", "103", "104", "174",
              "175"]

    if what_bus in busses:

        bus = bus_service(what_bus)
        bus1 = bus_route(what_bus)
        fail_count = 0
    else:
        # A failed  buss number increments the fail_count counter
        fail_count += 1
        print("How many times have we failed?: " + str(fail_count))
        # If they end up here they didnt enter a valid bus number
        # Ask them to re enter the bus number
        ######## This is still in error - need to work on this ################  - 17/05/2020 tw
        what_bus = input("Sorry thats not a Colchester bus. Please enter your bus number?: ")
        if what_bus in busses:
            bus = bus_route(what_bus)
            #bus = bus_service(what_bus)
        else:
            print("STILL IN ERROR!!!")


    # A little bit of Essex speak init
    print("\nBOSH!!!, Here's the bus you want geez. The number "  + bus[0] + " runs between " + bus[1] + " and "
          + bus[2])

def bus_service(bus_number):

    bus = bus_number
    # Try out retrieving a URL via urllib3
    # Use %s to pass in the Constants and Variables to make up the URL
    url = 'https://transportapi.com/v3/uk/bus/services/FESX:%s.json?app_id=%s&app_key=%s' % (bus, APP_ID, API_KEY)
    http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    response = http.request('GET', url)
    my_dict = json.loads(response.data.decode('utf-8'))
    outbound = my_dict['directions'][0]['destination']['description']
    inbound = my_dict['directions'][1]['destination']['description']

    # Return the bus number and its endpoints
    return bus_number, outbound, inbound

def next_bus_live():
    # URL to retrieve data. This mayy need more paramaters to be passed in. Currently only APP_ID and API_KEY
    url = 'https://transportapi.com/v3/uk/bus/stop/1500AA20/live.json?app_id=%s&app_key=%s&group=route&nextbuses=yes' % ( APP_ID, API_KEY)

    http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    response = http.request('GET', url)
    next_bus_live_dict = json.loads(response.data.decode('utf-8'))
    print(next_bus_live_dict)


def next_bus_timetabled():
    # URL to retrieve data. This may need more paramaters to be passed in. Currently only APP_ID and API_KEY
    url = 'https://transportapi.com/v3/uk/bus/stop/1500AA20/2020-05-15/07:10/timetable.json?app_id=%s&app_key=%s' % (APP_ID, API_KEY)

    http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    response = http.request('GET', url)
    next_bus_timetabled_dict = json.loads(response.data.decode('utf-8'))
    print(next_bus_timetabled_dict)

def bus_route(bus_number):

    bus1 = bus_number
    # Try out retrieving a URL via urllib3
    # Use %s to pass in the Constants and Variables to make up the URL
    url = 'https://transportapi.com/v3/uk/bus/route/FESX/%s/outbound/1500AA20/2020-05-15/07:10/timetable.json?' \
          'app_id=%s&app_key=%s&edge_geometry=false&stops=ALL' % (bus1, APP_ID, API_KEY)

    http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    response = http.request('GET', url)
    my_dict = json.loads(response.data.decode('utf-8'))
    for stop in my_dict['stops']:
        print("The bus is at the " + stop['stop_name'] + " stop at " + stop['time'])
        print("The bus stop is at lat/long " + str(stop['latitude']) + "," + str(stop['longitude']))



if __name__ == '__main__':
    main()