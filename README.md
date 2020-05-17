# buber
Bus Finder app for CodeInPlace 2020
This is the finl project code for my submission to CodeInPlace 2020
A course to introduce the participant to Python

# Description:
An application to provide information on specific bus numbers
through Colchester, Essex, UK


This will be done with the help of the transportapi
https://developer.transportapi.com/

## Basic Decomposition: - "Eat the elephant one bite at a time" 
1. Hold API key and Program ID so we dont need to keep entering it or URLS - DONE
2. Retreive data for the Number 65 bus heading outbound - DONE
3. Take user input for bus number. Only allow them to enter the busses we have supplied - DONE
    3.1 If user enter an incorrect bus number twice offer them the option to find the bus number by final destination
4. User enters a bus number - program tells user where bus comes and goes to and the departure time (from Town Center)
5. User enters a destination - Program tells user what bus goes there and when the next departure is (from Town Center)
6. Display data to user on a map. - Milestone 1

## Questions the app should be able to answer
1. When is the next bus - enter bus number return next bus time for town center location
2. Given a location display what busses go there. if you select a bus then display the time of the next bus

## Future work if we have time
1. Make a windows graphical app
2. Make an android graphical app
3. Deploy it to a virtual android phone and run it

## Tools/Frameworks
1. Kivy Framework - https://realpython.com/mobile-app-kivy-python/
2. Android dev app - https://developer.android.com/studio
