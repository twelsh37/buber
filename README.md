# buber
Bus Finder app for CodeInPlace 2020.
This code started as my  final project code for Stanfords CodeInPlace 2020
A course to introduce the participant to Python

# Description:
This application aims to provide bus users with an easy to use application that will allow them to retrievce information on specific bus journeys. 

The Application will start out covering the Colchester Area and buses to and from it via First Essex busses. 
It will then be expanded to provide bus information from further afield with the ultimate goal of providing bus information for the UK.

## Basic Decomposition: - "Eat the elephant one bite at a time" 
1. Hold API key and Program ID so we dont need to keep entering it or URLS - DONE
2. Retreive data for the Number 65 bus heading outbound - DONE
3. Take user input for bus number. Only allow them to enter the busses we have supplied - DONE<br>
    3.1 If user enter an incorrect bus number twice offer them the option to find the bus number by final destination -TBD
4. User enters a bus number - program tells user where bus comes and goes to and the departure time (from Town Center)- DONE
5. User enters a destination - Program tells user what bus goes there and when the next departure is (from Town Center) TBD
6. Display data to user on a map. - Milestone 1 -DONE

## Questions the app should be able to answer
1. When is the next bus - enter bus number return next bus time for town center location
2. Given a location display what busses go there. if you select a bus then display the time of the next bus

## Future work
1. Make a windows graphical app
2. Make an android graphical app
3. Deploy it to a virtual android phone and run it
4. Make web-enabled app

## Possible Tools/Frameworks
1. Kivy Framework - https://realpython.com/mobile-app-kivy-python/
2. Android dev app - https://developer.android.com/studio

## If you copy the code
Please feel free to fork or download the code. Im all for collabaration.
In order to run the code though you will have to get an application IF, APP_ID and API_KEY from transportapi.com.
When you have these you need to create a file called buberconfig.py and put the keys in there. This prevents us from passing our API keys around in the code.

The file should look something like this

buberconfig.py<br>
```python
# .gitignore should include reference to buberconfig.py
APP_ID = '<YOUR APP_ID>'
API_KEY = '<YOUR API_KEY>
```
