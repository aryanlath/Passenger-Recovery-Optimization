# Passenger-Recovery-Optimization


## Business Rules Engine using Streamlit

A GUI to easily modify the various scores for each attribute used to calculate PNR scores, flight grades, class allocation etc.






### Deployment

Make sure you have streamlit library installed or install it using the following command in the terminal
```bash
  pip install streamlit
```
Now, to run the script enter the following command in the terminal
```bash
  streamlit run landingPage.py
```




### Working

Files:
 
 - [landingPage.py](landingPage.py)
 - [PNRScore.py](pages/PNRScore.py)
 - [cabinAndClasses.py](pages/cabinAndClasses.py)
 - [flightScore.py](pages/flightScore.py)

Each file contains widgets to adjust various parameters along with some default values. On pressing the proceed button at the bottom of each page, all the values chosen are written into a python file as variables which can be imported for use in other programs.
 ### LandingPage.py
 - Main page of the GUI
 - Used to modify cabin allocation and maximum departure delay.
 - Writes to default.py.

 ### PNRScore.py
- Used to modify scores for PNR priority calculation parameters like PAX, loyalty, classes, MCT, MAXCT, ETD etc.
- writes to constants.py.

### cabinAndClasses.py
- Used to allow/disallow class changes during flight allocation and upgrade/downgrade rules.
- writes to classRules.py.

### flightScore.py
- Used to modify parameters used to rank the flight and allocate grades like arrival delay, STD and citypairs.
- writes to flightScores.py.
######


 

### Screenshots

![Landing Page](/readmeSS/Landing_Page_SS.png)
![PNR Scores](/readmeSS/PNRScore_SS.png)
![Flight Scores](/readmeSS/FlightScores_SS.png)
![Cabins and Classes](/readmeSS/CabinClasses_SS.png)



