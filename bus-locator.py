"""
Filename: bus-locator.py

### Description: ###
An application to provide information onspecific bus numbers
through Colchester, Essex, UK

This will be done with the help of the transportapi
https://developer.transportapi.com/

### Basic Decomposition: - "Eat the elephant one bite at a time" ###
1. Hold API key and Program ID so we dont need to keep entering it or URLS - DONE
2. Retreive data for the Number 65 bus heading outbound - DONE
3. Take user input for bus number. Only allow then to enter the busses we have supplied - DONE
    3.1 If user enter an incorrect bus number twice offer them the option to find the bus number by final destination
4. User enters a bus number - program tells user where bus comes and goes to and the departure time (from Town Center)
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

"""
# Import Libraries we need
import urllib3
import json



# Constants
APP_ID = '9e91c41c'
API_KEY = 'ebaa5b9461f7f42778146f909073d17a'

def main():

    # variables for main
    fail_count = 0

    # define a list of valid Colchester busses that we will accept
    busses =["17", "61", "62", "62A", "62B", "62C", "64", "64A", "65", "66", "66B", "67", "67B", "67C", "68", "70",
             "71", "71A", "71C", "71X", "74B", "75", "75A", "76", "88", "88A", "88B", "102", "103", "104", "174",
             "175"]
    # Ask the user to input a bus number
    what_bus = input("What bus do you want?: ")

    # Evaluate the user input
    # Is the users bus selection in our busses list? if yes, then proced
    if what_bus in busses:
        bus = bus_service(what_bus)
        fail_count = 0
    else:
        # A failed  buss number increments the fail_count counter
        fail_count += 1
        print("How many times have we failed?: " + str(fail_count))
        # If they end up here they didnt enter a valid bus number
        # Ask them to re enter the bus number
        what_bus = input("Sorry thats not a Colchester bus. Please enter your bus number?: ")
        if what_bus in busses:
            bus = bus_service(what_bus)
        else:
            print("STILL IN ERROR!!!")
    # A little bit of Essex speak init
    print("BOSH!!!, Here's the bus you want geez: ", bus)

def bus_service(bus_number):

    bus = bus_number
    # Try out retrieving a URL via urllib3
    # Use %s to pass in the Constants and Variables to make up the URL
    url = 'https://transportapi.com/v3/uk/bus/services/FESX:%s.json?app_id=%s&app_key=%s' % (bus,APP_ID,API_KEY)
    http = urllib3.PoolManager()

    # Request our data, and decode the json data returned
    response = http.request('GET', url)
    my_dict = json.loads(response.data.decode('utf-8'))
    #print(my_dict)
    # set up a key and values so we can call them by name
    # below returns the value of the key 'line' which is
    # our bus Number 65
    key = list(my_dict.keys())
    values = list(my_dict.values())
    #print(values[key.index("line")])
    print(values[key.index("directions")])
    # A little bit of Essex speak init
    #print("Its only the fucking bus init geez: %s" % values[key.index("line")])
    return bus_number


if __name__ == '__main__':
    main()