import urllib3
import json
import datetime
import folium
import pandas as pd

"""
TRANSPORT API
1. This URL identifies One particular bus service, identified by line and operator - Function bus_service()
It can be used to get the BUS_START and BUS_END of the journey
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


# Constants
APP_ID = '9e91c41c'
API_KEY = 'ebaa5b9461f7f42778146f909073d17a'
BASE_URL = 'https://transportapi.com/v3/uk/bus'


def main():
    #api_to_dataframe()
    #bus_service(65)
    #next_bus_live()
    #next_bus_timetabled()
    bus_route()

    #url = 'https://transportapi.com/v3/uk/bus/route/FESX/%s/outbound/1500AA20/2020-05-15/07:10/timetable.json?app_id=%s&app_key=%s&edge_geometry=false&stops=ALL'

    #http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    #response = http.request('GET', url)
    #my_dict = json.loads(response.data.decode('utf-8'))


    ## just a scratchpad for tgyrying thiungs out
    #my_dict = {'request_time': '2020-05-17T21:49:24+01:00', 'operator': 'FESX', 'operator_name': 'First Essex', 'line': '65', 'line_name': '65', 'origin_atcocode': '1500AA20', 'dir': 'outbound', 'stops': [{'time': '07:26', 'date': '2020-05-15', 'atcocode': '1500AA20', 'name': 'Causton Road', 'stop_name': 'Causton Road', 'smscode': 'esxamptg', 'locality': 'Colchester', 'bearing': 'N', 'indicator': 'opp', 'latitude': 51.89518, 'longitude': 0.89575}, {'time': '07:27', 'date': '2020-05-15', 'atcocode': '150033039010', 'name': 'The Albert', 'stop_name': 'The Albert', 'smscode': 'esxampwg', 'locality': 'Colchester', 'bearing': 'N', 'indicator': 'opp', 'latitude': 51.89682, 'longitude': 0.89547}, {'time': '07:29', 'date': '2020-05-15', 'atcocode': '150033095001', 'name': 'Railway Station Layby (Stand Ea)', 'stop_name': 'Railway Station Layby', 'smscode': 'esxamdpt', 'locality': 'Colchester', 'bearing': 'N', 'indicator': 'Stand Ea', 'latitude': 51.89965, 'longitude': 0.89489}, {'time': '07:29', 'date': '2020-05-15', 'atcocode': '1500DGK189', 'name': 'Bruff Close', 'stop_name': 'Bruff Close', 'smscode': 'esxgwdta', 'locality': 'Colchester', 'bearing': 'NE', 'indicator': 'E-bound', 'latitude': 51.90235, 'longitude': 0.89618}, {'time': '07:31', 'date': '2020-05-15', 'atcocode': '150033012007', 'name': 'Turner Rise', 'stop_name': 'Turner Rise', 'smscode': 'esxajwdm', 'locality': 'Colchester', 'bearing': 'NE', 'indicator': 'opp', 'latitude': 51.9044, 'longitude': 0.90105}, {'time': '07:32', 'date': '2020-05-15', 'atcocode': '150033012006', 'name': 'Wryneck Close', 'stop_name': 'Wryneck Close', 'smscode': 'esxajwdj', 'locality': 'Colchester', 'bearing': 'N', 'indicator': 'opp', 'latitude': 51.90722, 'longitude': 0.9027}, {'time': '07:33', 'date': '2020-05-15', 'atcocode': '1500IM578', 'name': 'General Hospital - main Rd', 'stop_name': 'General Hospital - main Rd', 'smscode': 'esxajwda', 'locality': 'Colchester', 'bearing': 'N', 'indicator': 'o/s', 'latitude': 51.9099, 'longitude': 0.90234}, {'time': '07:33', 'date': '2020-05-15', 'atcocode': '150033012003', 'name': 'Kingswood Road', 'stop_name': 'Kingswood Road', 'smscode': 'esxajwat', 'locality': 'Colchester', 'bearing': 'N', 'indicator': 'opp', 'latitude': 51.91238, 'longitude': 0.90191}, {'time': '07:34', 'date': '2020-05-15', 'atcocode': '150033003004', 'name': 'Thornwood', 'stop_name': 'Thornwood', 'smscode': 'esxajtwd', 'locality': 'Mile End, Colchester', 'bearing': 'NE', 'indicator': 'opp', 'latitude': 51.91506, 'longitude': 0.90089}, {'time': '07:35', 'date': '2020-05-15', 'atcocode': '150033003002', 'name': 'Bedford Road', 'stop_name': 'Bedford Road', 'smscode': 'esxajtpw', 'locality': 'Mile End, Colchester', 'bearing': 'NE', 'indicator': 'opp', 'latitude': 51.91672, 'longitude': 0.90424}, {'time': '07:36', 'date': '2020-05-15', 'atcocode': '1500OXLEYPAR', 'name': 'The Water Tower', 'stop_name': 'The Water Tower', 'smscode': 'esxjdawg', 'locality': 'Mile End, Colchester', 'bearing': 'NE', 'indicator': 'o/s', 'latitude': 51.91978, 'longitude': 0.91}, {'time': '07:37', 'date': '2020-05-15', 'atcocode': '150033004001', 'name': 'Julian Avenue', 'stop_name': 'Julian Avenue', 'smscode': 'esxajtpj', 'locality': 'Mile End, Colchester', 'bearing': 'NE', 'indicator': 'opp', 'latitude': 51.92143, 'longitude': 0.91557}, {'time': '07:37', 'date': '2020-05-15', 'atcocode': '150033004901', 'name': 'Matchett Drive', 'stop_name': 'Matchett Drive', 'smscode': 'esxjpdwp', 'locality': 'Mile End, Colchester', 'bearing': 'E', 'indicator': 'adj', 'latitude': 51.92226, 'longitude': 0.91822}, {'time': '07:39', 'date': '2020-05-15', 'atcocode': '150033006003', 'name': 'Newcomen Way', 'stop_name': 'Newcomen Way', 'smscode': 'esxajtpg', 'locality': 'Colchester', 'bearing': 'S', 'indicator': 'adj', 'latitude': 51.91946, 'longitude': 0.92109}, {'time': '07:39', 'date': '2020-05-15', 'atcocode': '150033006002', 'name': 'Oyster Business Park', 'stop_name': 'Oyster Business Park', 'smscode': 'esxajtpd', 'locality': 'Colchester', 'bearing': 'SE', 'indicator': 'adj', 'latitude': 51.91798, 'longitude': 0.92252}, {'time': '07:40', 'date': '2020-05-15', 'atcocode': '1500IM585', 'name': 'Brinkley Lane', 'stop_name': 'Brinkley Lane', 'smscode': 'esxajwgm', 'locality': 'Highwoods, Colchester', 'bearing': 'SW', 'indicator': 'SW-bound', 'latitude': 51.91628, 'longitude': 0.92273}, {'time': '07:40', 'date': '2020-05-15', 'atcocode': '1500DGK219', 'name': 'Regents Close', 'stop_name': 'Regents Close', 'smscode': 'esxjawdm', 'locality': 'Highwoods, Colchester', 'bearing': 'SE', 'indicator': 'adj', 'latitude': 51.91534, 'longitude': 0.92219}, {'time': '07:41', 'date': '2020-05-15', 'atcocode': '1500IM1198B', 'name': 'Berkley Close', 'stop_name': 'Berkley Close', 'smscode': 'esxajwgp', 'locality': 'Highwoods, Colchester', 'bearing': 'S', 'indicator': 'adj', 'latitude': 51.9135, 'longitude': 0.92349}, {'time': '07:41', 'date': '2020-05-15', 'atcocode': '150033010003', 'name': 'Derwent Road', 'stop_name': 'Derwent Road', 'smscode': 'esxajwgw', 'locality': 'Highwoods, Colchester', 'bearing': 'S', 'indicator': 'S-bound', 'latitude': 51.91228, 'longitude': 0.92295}, {'time': '07:43', 'date': '2020-05-15', 'atcocode': '150033009004', 'name': 'Baronia Croft', 'stop_name': 'Baronia Croft', 'smscode': 'esxajwmj', 'locality': 'Highwoods, Colchester', 'bearing': 'S', 'indicator': 'adj', 'latitude': 51.90868, 'longitude': 0.92158}, {'time': '07:43', 'date': '2020-05-15', 'atcocode': '1500IM568Y', 'name': 'Pinecroft Gardens', 'stop_name': 'Pinecroft Gardens', 'smscode': 'esxgwjtj', 'locality': 'Highwoods, Colchester', 'bearing': 'W', 'indicator': 'opp', 'latitude': 51.90754, 'longitude': 0.91765}, {'time': '07:44', 'date': '2020-05-15', 'atcocode': '150033009002', 'name': 'Victoria Gardens', 'stop_name': 'Victoria Gardens', 'smscode': 'esxajwmd', 'locality': 'Highwoods, Colchester', 'bearing': 'NW', 'indicator': 'opp', 'latitude': 51.90959, 'longitude': 0.91485}, {'time': '07:45', 'date': '2020-05-15', 'atcocode': '150033009001', 'name': 'Spindle Wood', 'stop_name': 'Spindle Wood', 'smscode': 'esxajwma', 'locality': 'Highwoods, Colchester', 'bearing': 'E', 'indicator': 'adj', 'latitude': 51.91164, 'longitude': 0.91501}, {'time': '07:47', 'date': '2020-05-15', 'atcocode': '1500IM2456B', 'name': 'Highwood Square (Stop 3)', 'stop_name': 'Highwood Square', 'smscode': 'esxjawma', 'locality': 'Highwoods, Colchester', 'bearing': 'NW', 'indicator': 'Stop 3', 'latitude': 51.91048, 'longitude': 0.91805}], 'id': 'https://transportapi.com/v3/uk/bus/route/FESX/65/outbound/1500AA20/2020-05-15/07:10/timetable.json?app_id=9e91c41c&app_key=ebaa5b9461f7f42778146f909073d17a'}
    location_dict = {'Causton Road' : ['51.89518','0.89575'],'The Albert' : ['51.89682','0.89547'],'Railway Station Layby' : ['51.89965','0.89489'],'Bruff Close' : ['51.90235','0.89618'],'Turner Rise' : ['51.9044','0.90105'],'Wryneck Close' : ['51.90722','0.9027'],'General Hospital - main Rd' : ['51.9099','0.90234'],'Kingswood Road' : ['51.91238','0.90191'],'Thornwood' : ['51.91506','0.90089'],'Bedford Road' : ['51.91672','0.90424'],'The Water Tower' : ['51.91978','0.91'],'Julian Avenue' : ['51.92143','0.91557'],'Matchett Drive' : ['51.92226','0.91822'],'Newcomen Way' : ['51.91946','0.92109'],'Oyster Business Park' : ['51.91798','0.92252'],'Brinkley Lane' : ['51.91628','0.92273'],'Regents Close' : ['51.91534','0.92219'],'Berkley Close' : ['51.9135','0.92349'],'Derwent Road' : ['51.91228','0.92295'],'Baronia Croft' : ['51.90868','0.92158'],'Pinecroft Gardens' : ['51.90754','0.91765'],'Victoria Gardens' : ['51.90959','0.91485'],'Spindle Wood' : ['51.91164','0.91501'],'Highwood Square' : ['51.91048','0.91805']}

    # While loop to return values in a dict, with a list of dicts
    #i = 0
    #print("My dictionary length is: " + str(len(my_dict['stops'])))
    #while i < len(my_dict['stops']):
    #    location_dict.update({stop['stop_name'] : stop['latitude'], stop['longitude']})
        #print(location_dict)
        #print("The bus is at the " + my_dict['stops'][i]['stop_name'] + " stop at " + my_dict['stops'][i]['time'])
        #print("The bus stop is at lat/long: " + str(my_dict['stops'][i]['latitude']) + "," + str(my_dict['stops'][i]['longitude']))

        #i = i + 1

    # same as above but using a for loop - Less typing in this one and no variable for a counter
    #for stop in my_dict['stops']:
    #    print(stop['stop_name'] + "," +  str(stop['latitude']) + "," + str(stop['longitude']))

        # testing out folium
        #route_65 = folium.Map(location=[stop['latitude'], stop['longitude']], zoom_start=20)
        # Pass a string in popup parameter
        #folium.Marker([stop['latitude'], stop['longitude']], popup=stop['stop_name']).add_to(route_65)
        # Save the output to an html file
        #route_65.save(" route_65.html ")

        # Import location csv data into pandas
        #df_location = pd.read_csv('location.csv')
        # Check we got it
        #print(df_location.head())

        # Prep data for the map
        #locations = df_location[['lat', 'long']]
        #locationlist = locations.values.tolist()
        #print(len(locationlist))

        # Now build the map
        #route_65 = folium.Map(location=[51.89518, 0.89575 ], zoom_start=14)
        #for point in range(0, len(locationlist)):
        #    folium.Marker(locationlist[point], popup=stop['stop_name']).add_to(route_65)
        #    route_65.save(" route_65.html ")

def bus_service(bus_number):
    bus = bus_number
    # Try out retrieving a URL via urllib3
    # Use %s to pass in the Constants and Variables to make up the URL
    url = BASE_URL + '/services/FESX:%s.json?app_id=%s&app_key=%s' % (bus, APP_ID, API_KEY)
    http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    response = http.request('GET', url)
    bus_service_dict = json.loads(response.data.decode('utf-8'))
    print(bus_service_dict)

def next_bus_live():
    # URL to retrieve data. This may need more paramaters to be passed in. Currently only APP_ID and API_KEY
    url = BASE_URL + '/stop/1500AA20/live.json?app_id=%s&app_key=%s&group=route&nextbuses=yes' % ( APP_ID, API_KEY)

    http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    response = http.request('GET', url)
    next_bus_live_dict = json.loads(response.data.decode('utf-8'))
    print(next_bus_live_dict)


def next_bus_timetabled():
    # URL to retrieve data. This may need more paramaters to be passed in. Currently only APP_ID and API_KEY
    url = BASE_URL + '/stop/1500AA20/2020-05-15/07:10/timetable.json?app_id=%s&app_key=%s' % (APP_ID, API_KEY)

    http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    response = http.request('GET', url)
    next_bus_timetabled_dict = json.loads(response.data.decode('utf-8'))
    print(next_bus_timetabled_dict)

def bus_route():
    current_date = datetime.date.today()
    current_date = current_date.strftime("%Y-%m-%d")

    bus_number = 74
    # URL to retrieve data. This may need more paramaters to be passed in. Currently only APP_ID and API_KEY
    url = BASE_URL + '/route/FESX/%s/outbound/150033038003/%s/07:37/timetable.json?app_id=%s&app_key=%s&edge_geometry=false&stops=ALL' % (bus_number,current_date,APP_ID, API_KEY)

    http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    response = http.request('GET', url)
    bus_route_dict = json.loads(response.data.decode('utf-8'))
    #print(bus_route_dict)

    i = 0
    while i < len(bus_route_dict['stops']):
        #location_dict.update({stop['stop_name'] : stop['latitude'], stop['longitude']})
        #print(location_dict)
        print("The bus is at the " + bus_route_dict['stops'][i]['stop_name'] + " stop at " + bus_route_dict['stops'][i]['time'])
        print("The bus stop is at lat/long: " + str(bus_route_dict['stops'][i]['latitude']) + "," + str(bus_route_dict['stops'][i]['longitude']))

        i = i + 1

def api_to_dataframe():
    #temp bus for testing. TThis should be passed in as required
    bus1 = 65

    # this is the bus_route() function URL
    url = BASE_URL + '/route/FESX/%s/outbound/1500AA20/2020-05-15/07:10/timetable.json?app_id=%s&app_key=%s' \
                     '&edge_geometry=false&stops=ALL' % (bus1, APP_ID, API_KEY)

    http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    response = http.request('GET', url)
    api_resp_dict = json.loads(response.data.decode('utf-8'))

    for stop in api_resp_dict['stops']:
        print(stop['stop_name'] + "," +  str(stop['latitude']) + "," + str(stop['longitude']))

    #print(api_resp_dict['stops'])
    #df = pd.DataFrame(x['stops'])
    #print(df.head())

if __name__ == '__main__':
    main()