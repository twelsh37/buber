﻿import folium
import pandas as pd

## just a scratchpad for tgyrying thiungs out
my_dict = {'request_time': '2020-05-17T21:49:24+01:00', 'operator': 'FESX', 'operator_name': 'First Essex', 'line': '65', 'line_name': '65', 'origin_atcocode': '1500AA20', 'dir': 'outbound', 'stops': [{'time': '07:26', 'date': '2020-05-15', 'atcocode': '1500AA20', 'name': 'Causton Road', 'stop_name': 'Causton Road', 'smscode': 'esxamptg', 'locality': 'Colchester', 'bearing': 'N', 'indicator': 'opp', 'latitude': 51.89518, 'longitude': 0.89575}, {'time': '07:27', 'date': '2020-05-15', 'atcocode': '150033039010', 'name': 'The Albert', 'stop_name': 'The Albert', 'smscode': 'esxampwg', 'locality': 'Colchester', 'bearing': 'N', 'indicator': 'opp', 'latitude': 51.89682, 'longitude': 0.89547}, {'time': '07:29', 'date': '2020-05-15', 'atcocode': '150033095001', 'name': 'Railway Station Layby (Stand Ea)', 'stop_name': 'Railway Station Layby', 'smscode': 'esxamdpt', 'locality': 'Colchester', 'bearing': 'N', 'indicator': 'Stand Ea', 'latitude': 51.89965, 'longitude': 0.89489}, {'time': '07:29', 'date': '2020-05-15', 'atcocode': '1500DGK189', 'name': 'Bruff Close', 'stop_name': 'Bruff Close', 'smscode': 'esxgwdta', 'locality': 'Colchester', 'bearing': 'NE', 'indicator': 'E-bound', 'latitude': 51.90235, 'longitude': 0.89618}, {'time': '07:31', 'date': '2020-05-15', 'atcocode': '150033012007', 'name': 'Turner Rise', 'stop_name': 'Turner Rise', 'smscode': 'esxajwdm', 'locality': 'Colchester', 'bearing': 'NE', 'indicator': 'opp', 'latitude': 51.9044, 'longitude': 0.90105}, {'time': '07:32', 'date': '2020-05-15', 'atcocode': '150033012006', 'name': 'Wryneck Close', 'stop_name': 'Wryneck Close', 'smscode': 'esxajwdj', 'locality': 'Colchester', 'bearing': 'N', 'indicator': 'opp', 'latitude': 51.90722, 'longitude': 0.9027}, {'time': '07:33', 'date': '2020-05-15', 'atcocode': '1500IM578', 'name': 'General Hospital - main Rd', 'stop_name': 'General Hospital - main Rd', 'smscode': 'esxajwda', 'locality': 'Colchester', 'bearing': 'N', 'indicator': 'o/s', 'latitude': 51.9099, 'longitude': 0.90234}, {'time': '07:33', 'date': '2020-05-15', 'atcocode': '150033012003', 'name': 'Kingswood Road', 'stop_name': 'Kingswood Road', 'smscode': 'esxajwat', 'locality': 'Colchester', 'bearing': 'N', 'indicator': 'opp', 'latitude': 51.91238, 'longitude': 0.90191}, {'time': '07:34', 'date': '2020-05-15', 'atcocode': '150033003004', 'name': 'Thornwood', 'stop_name': 'Thornwood', 'smscode': 'esxajtwd', 'locality': 'Mile End, Colchester', 'bearing': 'NE', 'indicator': 'opp', 'latitude': 51.91506, 'longitude': 0.90089}, {'time': '07:35', 'date': '2020-05-15', 'atcocode': '150033003002', 'name': 'Bedford Road', 'stop_name': 'Bedford Road', 'smscode': 'esxajtpw', 'locality': 'Mile End, Colchester', 'bearing': 'NE', 'indicator': 'opp', 'latitude': 51.91672, 'longitude': 0.90424}, {'time': '07:36', 'date': '2020-05-15', 'atcocode': '1500OXLEYPAR', 'name': 'The Water Tower', 'stop_name': 'The Water Tower', 'smscode': 'esxjdawg', 'locality': 'Mile End, Colchester', 'bearing': 'NE', 'indicator': 'o/s', 'latitude': 51.91978, 'longitude': 0.91}, {'time': '07:37', 'date': '2020-05-15', 'atcocode': '150033004001', 'name': 'Julian Avenue', 'stop_name': 'Julian Avenue', 'smscode': 'esxajtpj', 'locality': 'Mile End, Colchester', 'bearing': 'NE', 'indicator': 'opp', 'latitude': 51.92143, 'longitude': 0.91557}, {'time': '07:37', 'date': '2020-05-15', 'atcocode': '150033004901', 'name': 'Matchett Drive', 'stop_name': 'Matchett Drive', 'smscode': 'esxjpdwp', 'locality': 'Mile End, Colchester', 'bearing': 'E', 'indicator': 'adj', 'latitude': 51.92226, 'longitude': 0.91822}, {'time': '07:39', 'date': '2020-05-15', 'atcocode': '150033006003', 'name': 'Newcomen Way', 'stop_name': 'Newcomen Way', 'smscode': 'esxajtpg', 'locality': 'Colchester', 'bearing': 'S', 'indicator': 'adj', 'latitude': 51.91946, 'longitude': 0.92109}, {'time': '07:39', 'date': '2020-05-15', 'atcocode': '150033006002', 'name': 'Oyster Business Park', 'stop_name': 'Oyster Business Park', 'smscode': 'esxajtpd', 'locality': 'Colchester', 'bearing': 'SE', 'indicator': 'adj', 'latitude': 51.91798, 'longitude': 0.92252}, {'time': '07:40', 'date': '2020-05-15', 'atcocode': '1500IM585', 'name': 'Brinkley Lane', 'stop_name': 'Brinkley Lane', 'smscode': 'esxajwgm', 'locality': 'Highwoods, Colchester', 'bearing': 'SW', 'indicator': 'SW-bound', 'latitude': 51.91628, 'longitude': 0.92273}, {'time': '07:40', 'date': '2020-05-15', 'atcocode': '1500DGK219', 'name': 'Regents Close', 'stop_name': 'Regents Close', 'smscode': 'esxjawdm', 'locality': 'Highwoods, Colchester', 'bearing': 'SE', 'indicator': 'adj', 'latitude': 51.91534, 'longitude': 0.92219}, {'time': '07:41', 'date': '2020-05-15', 'atcocode': '1500IM1198B', 'name': 'Berkley Close', 'stop_name': 'Berkley Close', 'smscode': 'esxajwgp', 'locality': 'Highwoods, Colchester', 'bearing': 'S', 'indicator': 'adj', 'latitude': 51.9135, 'longitude': 0.92349}, {'time': '07:41', 'date': '2020-05-15', 'atcocode': '150033010003', 'name': 'Derwent Road', 'stop_name': 'Derwent Road', 'smscode': 'esxajwgw', 'locality': 'Highwoods, Colchester', 'bearing': 'S', 'indicator': 'S-bound', 'latitude': 51.91228, 'longitude': 0.92295}, {'time': '07:43', 'date': '2020-05-15', 'atcocode': '150033009004', 'name': 'Baronia Croft', 'stop_name': 'Baronia Croft', 'smscode': 'esxajwmj', 'locality': 'Highwoods, Colchester', 'bearing': 'S', 'indicator': 'adj', 'latitude': 51.90868, 'longitude': 0.92158}, {'time': '07:43', 'date': '2020-05-15', 'atcocode': '1500IM568Y', 'name': 'Pinecroft Gardens', 'stop_name': 'Pinecroft Gardens', 'smscode': 'esxgwjtj', 'locality': 'Highwoods, Colchester', 'bearing': 'W', 'indicator': 'opp', 'latitude': 51.90754, 'longitude': 0.91765}, {'time': '07:44', 'date': '2020-05-15', 'atcocode': '150033009002', 'name': 'Victoria Gardens', 'stop_name': 'Victoria Gardens', 'smscode': 'esxajwmd', 'locality': 'Highwoods, Colchester', 'bearing': 'NW', 'indicator': 'opp', 'latitude': 51.90959, 'longitude': 0.91485}, {'time': '07:45', 'date': '2020-05-15', 'atcocode': '150033009001', 'name': 'Spindle Wood', 'stop_name': 'Spindle Wood', 'smscode': 'esxajwma', 'locality': 'Highwoods, Colchester', 'bearing': 'E', 'indicator': 'adj', 'latitude': 51.91164, 'longitude': 0.91501}, {'time': '07:47', 'date': '2020-05-15', 'atcocode': '1500IM2456B', 'name': 'Highwood Square (Stop 3)', 'stop_name': 'Highwood Square', 'smscode': 'esxjawma', 'locality': 'Highwoods, Colchester', 'bearing': 'NW', 'indicator': 'Stop 3', 'latitude': 51.91048, 'longitude': 0.91805}], 'id': 'https://transportapi.com/v3/uk/bus/route/FESX/65/outbound/1500AA20/2020-05-15/07:10/timetable.json?app_id=9e91c41c&app_key=ebaa5b9461f7f42778146f909073d17a'}
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
for stop in my_dict['stops']:
    print(stop['stop_name'] + "," +  str(stop['latitude']) + "," + str(stop['longitude']))

    # testing out folium
    #route_65 = folium.Map(location=[stop['latitude'], stop['longitude']], zoom_start=20)
    # Pass a string in popup parameter
    #folium.Marker([stop['latitude'], stop['longitude']], popup=stop['stop_name']).add_to(route_65)
    # Save the output to an html file
    #route_65.save(" route_65.html ")

    # Import location csv data into pandas
    df_location = pd.read_csv('location.csv')
    # Check we got it
    print(df_location.head())

    # Prep data for the map
    locations = df_location[['lat', 'long']]
    locationlist = locations.values.tolist()
    print(len(locationlist))

    # Now build the map
    route_65 = folium.Map(location=[51.89518, 0.89575 ], zoom_start=14)
    for point in range(0, len(locationlist)):
        folium.Marker(locationlist[point], popup=stop['stop_name']).add_to(route_65)
        route_65.save(" route_65.html ")







