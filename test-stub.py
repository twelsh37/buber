"""
Filename: test-stub.py

### Description: ###
This stub is used to test the URL's we are retrieving.
The idea here is to be able to paramaterise as much as possible.

Use %s to pass in the Constants and Variables to make up the URLS as much as possible

# IDEAS
1.0 Can we read in all national data to something like Pandas or numpy?
1.1 If we can, how do we sift data as we require?
1.2 If we cant use Pandas or Numpy will dictionaries be ok?

2.0 Both next_bus() and next_bus_timetabled() require atcocodes for the stops. how do we tie these in?
2.1 By region?
2.2 By Location, i.e Town/City
2.3 By Operator?

3.0

bus_service()
We should be able to select the Bus Operator i.e FESX field
url = BASE_URL + '/services/FESX:%s.json?app_id=%s&app_key=%s' % (bus_num, buberconfig.APP_ID, buberconfig.API_KEY)

# next_bus()
# url = BASE_URL + '/stop/1500AA20/live.json?app_id=buberconfig.APP_ID&app_key=buberconfig.API_KEY&group=route&' \
#                 'nextbuses=yes'

# next_bus_timetabled()

# url = BASE_URL + '/stop/1500AA20/%s/07:10/timetable.json?app_id=buberconfig.APP_ID&' \
#                 'app_key=buberconfig.API_KEY' % (TODAY, buberconfig.APP_ID, buberconfig.API_KEY)

# bus_route()
Has the concept of inbound and outbound directions. - This currently works but needs more paramaterising.
Outbound - Heading out from its depot /start point.
Inbound - Heading back to its depot / start point
requires a valid time for the servivce at the start point either Inbound or Outbound

# url = BASE_URL + '/route/FESX/%s/inbound/1500IM2349B/%s/06:40/timetable.json?app_id=%s&app_key=%s&' \
#                'edge_geometry=false&stops=ALL' % (bus, TODAY, buberconfig.APP_ID, buberconfig.API_KEY)

"""
# Import Libraries we need
import urllib3
import json

# Import our buberconfig
import buberconfig

# Constants
BASE_URL = 'https://transportapi.com/v3/uk/bus'

def main():
    bus_num = input(' Enter a number: ')

    # Retrieve a URL via urllib3
    # Use %s to pass in the Constants and Variables to make up the URL
    # bus_service() - We should be able to select the Bus Operator i.e FESX field
    url = BASE_URL + '/services/FESX:%s.json?app_id=%s&app_key=%s' % (bus_num, buberconfig.APP_ID, buberconfig.API_KEY)

    # next_bus()
    # url = BASE_URL + '/stop/1500AA20/live.json?app_id=buberconfig.APP_ID&app_key=buberconfig.API_KEY&group=route&' \
    #                 'nextbuses=yes'

    # next_bus_timetabled():
    # url = BASE_URL + '/stop/1500AA20/%s/07:10/timetable.json?app_id=buberconfig.APP_ID&' \
    #                 'app_key=buberconfig.API_KEY' % (TODAY, buberconfig.APP_ID, buberconfig.API_KEY)

    # bus_route()
    # url = BASE_URL + '/route/FESX/%s/inbound/1500IM2349B/%s/06:40/timetable.json?app_id=%s&app_key=%s&' \
    #                'edge_geometry=false&stops=ALL' % (bus, TODAY, buberconfig.APP_ID, buberconfig.API_KEY)



    http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    response = http.request('GET', url)
    bus_service_dict = json.loads(response.data.decode('utf-8'))
    outbound = bus_service_dict['directions'][0]['destination']['description']
    inbound = bus_service_dict['directions'][1]['destination']['description']

    # Return the bus number and its endpoints
    print('Bus Number:%s, Outbound:%s, Inbound:%s' % (bus_num, outbound, inbound))



if __name__ == '__main__':
    main()