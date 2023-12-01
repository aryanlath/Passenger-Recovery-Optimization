# Passenger-Recovery-Optimization

Airlines routinely change their flight schedules for various reasons like seasonal demands, to
pick new routes, time changes needed based on daylight savings, changes to flight numbers,
operating frequency, timings, etc. Many passengers get impacted due these schedule
changes and they need to be regularly re-accommodated to alternate flights. 

The project uses a quantum computing based approach to identify optimal alternate flight solutions for all impacted passengers based on certain constraints and keeping in mind various factors like PNR priority, time to reach destination, special passenger types without jeopardising the flight experience for the passengers.


## Business Rules Engine using Streamlit

We have provided a GUI, deployed using `Streamlit` to easily modify the various scores for each attribute used to calculate PNR scores, flight grades, class allocation etc.


## Deployment

Make sure you have streamlit library installed or install it using the following command in the terminal
```bash
  pip install streamlit
```
Now, to run the script enter the following command in the terminal
```bash
  streamlit run landingPage.py
```


## Working

Each file contains widgets to adjust various parameters along with some default values. On pressing the proceed button at the bottom of each page, all the values chosen are written into a python file as variables which can be imported for use in other programs.
 ### LandingPage.py
 - Main page of the GUI
 - Used to modify cabin allocation and maximum departure delay.
 - **Writes to default.py**.
![Landing Page](/assets/Landing_Page_SS.png)
 ### PNRScore.py
- Used to modify scores for PNR priority calculation parameters like PAX, loyalty, classes, MCT, MAXCT, ETD etc.
- **writes to constants.py**.
![PNR Scores](/assets/PNRScore_SS.png)
### cabinAndClasses.py
- Used to allow/disallow class changes during flight allocation and upgrade/downgrade rules.
- **writes to classRules.py**.
![Cabins and Classes](/assets/CabinClasses_SS.png)
### flightScore.py
- Used to modify parameters used to rank the flight and allocate grades like arrival delay, STD and citypairs.
- **writes to flightScores.py**.
![Flight Scores](/assets/FlightScores_SS.png)


## Glossary

A few terms commonly used by airlines and what they mean

- PNR\
Passenger name necord data is unverified information provided by passengers and collected by air carriers to enable the reservation and check-in processes. The data is used by the air carriers to manage their air transportation services.

- Cabins\
Cabins divide every seat on a plane into different categories, each with its own price and set of rules. Fare cabins are identified by one-letter fare codes. There are four main cabins - First, Business, Premium Economy and Economy.

- Classes\
Each cabin is further divided various classes. They typically denote the level of service or fare type purchased by a passenger. The class often determines the amenities, seat comfort, services, and flexibility available during the flight.  







