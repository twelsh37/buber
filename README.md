# buber
Bus Finder app for CodeInPlace 2020.
This code started as my  final project code forC Stanfords CodeInPlace 2020
A course to introduce the participant to Python

# Description:
This application aims to provide bus users with an easy to use application that will allow them to retrievce information on specific bus journeys. 

The Application will start out covering teh Coplchester Area and vbusses to and from it via First Essex busses. 
It will then be expanded top provide bus information from gutryher afiels with the ultimate goal of providing bust information for the UK.

## Basic Decomposition: - "Eat the elephant one bite at a time" 
1. Hold API key and Program ID so we dont need to keep entering it or URLS - DONE
2. Retreive data for the Number 65 bus heading outbound - DONE
3. Take user input for bus number. Only allow them to enter the busses we have supplied - DONE<br>
    3.1 If user enter an incorrect bus number twice offer them the option to find the bus number by final destination -TBD
4. User enters a bus number - program tells user where bus comes and goes to and the departure time (from Town Center)- TBD
5. User enters a destination - Program tells user what bus goes there and when the next departure is (from Town Center) TBD
6. Display data to user on a map. - Milestone 1 -DONE

## Questions the app should be able to answer
1. When is the next bus - enter bus number return next bus time for town center location
2. Given a location display what busses go there. if you select a bus then display the time of the next bus

## Future work
1. Make a windows graphical app
2. Make an android graphical app
3. Deploy it to a virtual android phone and run it
4 Make website enabled

## Possible Tools/Frameworks
1. Kivy Framework - https://realpython.com/mobile-app-kivy-python/
2. Android dev app - https://developer.android.com/studio
