# IoT-Proyect-ITESM

## Team 10

### Introduction

The proyect consists in implementing a creative solution to the problem of finding a parking spot through a parking lot. Using an IoT approach, we used the Intel Edison development board to simulate the interaction between the different parts of the system. This parts consist on the following:

- A database 
- A cellphone application 
- Two web page
- A phsysical test model

The solution was implemented for the specific location of ITESM Campus Guadalajara. The data storage and services provided are thought to be used only by members of the ITESM community. Nevertheless, this is a scalable proyect and may be imporoved, or used as a template or a model basis to design your own solution to any place of your liking.  

### The Database

The database function is to stores the information of the users that register in the cellphone application, the zones that divide the parking lot, the number of parking spots, and the education sectors that are near each zone. It  interacts with the mobile application and the Edison to have an accurate count of parking spots that are available in the phsysical test model and efficiently assign the user to the nearest unoccupied place.

The service the we used to build the database was the free application Firebase.
You can find the link to the web page here [Firebase](https://www.firebase.com/).

Firebase use the Json syntax to store data. Our database structure looks as following.

- sectors

  - name
  - position

- users

  - name
  - email
  - id
  - plates
  - schedule

- zone

  - name 
  - position

### Cellphone Application

The cellphone application enables the any student or employee of the campus to use the parking service. It has a profile configuration that lets you choose the educational sectos you want to park near to, depending on the day of the week, and it indicates the zone with a free spot nearest to the location you specified.

It has been developed for Android using Android Studios and it's already available on the Play Store with the name *Spot*.
The link to Android Studio is the next one: [Android](http://developer.android.com/intl/es/index.html).

Through the Firebase docs Android [tutorial](https://www.firebase.com/docs/android/) we were easily able to manipulate the database through the application.

### The Edison

All the Edison-side code is written in Python. The following is a brief guide of how to use the code.

To create a process to serve the app requests run:

`python PQueue.py`
 
And to run a 2-zone example using sensors connected to 2 Edison boards run:

`python PQueue_demo.py`

and and the second Edison:

`python PQueue_demo_slave`

The code provided are only brief examples of want can be done. 

### The web pages

The administrators page was done in HTLM, CSS and JavaScript so that it can connect with the database. The page will help with giving out information in real time to the people in charge of security in that area. The administrator can know whether the parking lot is full or not and give an estimation of how many cars are parked in each of the areas of the parking lot. 

The teams web page was developed using programing languages such as HTML and CSS, this pages is just to give information about the team members and how we developed the idea for this system that we created.

We developed an app for the driver/user that needs to find a parking lot quickly. For this app, we used java for code and xml for the design. The objective of the app is help the user to find a parking lot where he needs to park. This means that depending on their schedule for that day, they app will recommend the user where to park and the user will let know the app whether they parked in that zone or not.

Contributions are encouraged!
