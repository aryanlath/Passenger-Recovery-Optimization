# Passenger-Recovery-Optimization

Airlines routinely change their flight schedules for various reasons like seasonal demands, picking new routes, time changes needed based on daylight savings, changes to flight numbers,
operating frequency, timings, etc. Many passengers get impacted due to these schedule
changes and they need to be regularly re-accommodated to alternate flights. 

The project uses a advanced and robust **Hybrid Classical-Quantum Solution** to identify optimal alternate flight solutions for all impacted passengers based on certain constraints and considering various factors like PNR priority, time to reach the destination, and special passenger types without jeopardizing the flight experience for the passengers.
[Report Link](https://drive.google.com/file/d/1sPOJW-YTl1KlpY3xH9R1-QTFlTAFfTzS/view?usp=sharing)

## Business Rules Engine using Streamlit

We have provided a GUI, deployed using `Streamlit` to provide **flexibility** and easily modify the ruleset containing various scores for each attribute used to calculate PNR scores, flight grades, class allocation, etc.


## Deployment

### Installing the dependencies
**Make sure that you have `Python 3.10` installed in your system**

Run the following command in the terminal
```
pip install -r requirements.txt
```

### Setting up the environment file

Make a file named `.env` in the main folder, it's content should be: (It has already been made in this case though)
```
GMAPS_API_KEY=m9E2S8UXfEJDX7zdwDBlHW1eoMDUOOzlCJBiEsnu6gPMEZzr6lE9FNC6SNgTjmly
DWAVE_TOKEN=DEV-3e05ad7ac21e02030bd41cdbfbbb9ee45989364f
flight_mail=rsinh1140@gmail.com
flight_mail_password=asku teig bixk iiwh
```
`GMAPS_API_KEY` can be obtained from the `First Distancematrix accurate application` API of [Distance Matrix](https://distancematrix.ai/)

`DWAVE_TOKEN` can be obtained from [here](https://cloud.dwavesys.com/leap/)

### Running the program
Now, to run the script enter the following command in the terminal
```bash
streamlit run Landing_Page.py
```


## Working

Each file contains widgets to adjust various parameters along with some default values.There is also a button indicating wheather we want to allow flights to adjacent city pairs in main page. On pressing the proceed button at the bottom of each page, all the values chosen are written into a python file as variables which can be imported for use in other programs.

### Landing_Page.py
- Used to generate different solution files and send email to the passengers.
- **Option to add different city pair solution**
  
![landing_page](./assets/Landing_Page_SS2.png)


 ### PNR_Score.py
- Used to modify scores for PNR priority calculation parameters like PAX, loyalty, classes, MCT, MAXCT, ETD, etc
- **writes to constants.py**
  
![PNR Scores](./assets/PNR_Score_SS2.png)

### Cabin_And_Classes.py
- Used to allow/disallow class changes during flight allocation and upgrade/downgrade rules
- **writes to classRules.py**
  
![Cabins and Classes](./assets/Cabin_Score_SS2.png)

### Flight_Score.py
- Used to modify parameters used to rank the flight and allocate grades like arrival delay, STD and citypairs
- **writes to flightScores.py**
  
![Flight Scores](./assets/Flight_Score_SS2.png)

### Solution_1.py
- Used to display PNR wise re-accomodation solution 
- **displays only after generating solution files**

Following this, we have 2 more pages corresponding to the other two solutions.
  
![Solution File](./assets/Solution_File_SS2.png)

### Statistics.py
- Used to display various plots which helps compare different solutions by our model.
- **displays only after generating solution files**
  
![Statistics](./assets/Statistics_SS2.png)



## Glossary

A few terms commonly used by airlines and what they mean

- **PNR**\
Passenger name record data is unverified information provided by passengers and collected by air carriers to enable the reservation and check-in processes. The data is used by the air carriers to manage their air transportation services.

- **Cabins**\
Cabins divide every seat on a plane into different categories, each with its own price and set of rules. Fare cabins are identified by one-letter fare codes. There are four main cabins - First, Business, Premium Economy and Economy.

- **Classes**\
Each cabin is further divided various classes. They typically denote the level of service or fare type purchased by a passenger. The class often determines the amenities, seat comfort, services, and flexibility available during the flight.  

- **PAX**\
PAX denotes the number of passengers attached to a single PNR.

- **SSR**\
SSR stands for Special Service Request. SSRs are codes used within the airline industry to communicate specific passenger or flight-related requests and information to the airline's reservation and operation systems.

- **Loyalty**\
Frequent travelers or passengers who consistently choose to fly with a particular airline or its partners are incentivized by given a loyalty class like gold, and silver. Passengers with a high loyalty class are given a higher preference by the airline.

- **MCT**\
Minimum Connection Time between two connecting flights.

- **MAXCT**\
Maximum Connection Time between two connecting flights.

- **ETD**\
Estimated time of departure of a planned flight.






