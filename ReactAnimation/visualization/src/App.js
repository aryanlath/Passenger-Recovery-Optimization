import React, { useState, useEffect } from 'react';
import file from './result_quantum_0.json' // JSON file having PNRs which were cancelled
import './styles.css';                       // CSS file
import icon from './passenger.png'              // Passenger icon
import plane from './plane.png'              // Flight icon


const convertNewFormat = (data) => {                    //Make flight object from JSON
  const entries = Object.keys(data).map((key) => {    

    const entry = data[key];                            //key == PNR Number
    let ids=[];                                         //Store inventory IDs
    let proparrivaltime=[];                             //Store Proposed Arrival Times
    let propdeparturetime=[];                           //Store Proposed Departure Times
    let hops=data[key].Proposed.length;                 //Get number of connecting flights
    
    for (let i=0;i<hops;i++)
    {
      ids.push(data[key].Proposed[i][0]);               //appending all inventory IDs to list
    }
    let propclass=[];
    for (let i=0;i<hops;i++)
    {
      propclass.push(data[key].Proposed[i][1]);         //appending all cabins to list
    }
    let propsubclass=[];
    for (let i=0;i<hops;i++)
    {
      propsubclass.push(data[key].Proposed[i][2]);      //appending all classes to list
      if (i!=hops-1)
      {
        propsubclass.push("#");
     }
    }
    for (let i=0;i<hops;i++)
    {
      proparrivaltime.push(data[key].Proposed[i][3]);   //appending all arrival times to list
      propdeparturetime.push(data[key].Proposed[i][4]); //appending all departure times to list
    }
    

    entry.ProposedID=ids;                               //Setting as attribute
    entry.ProposedClass=propclass;
    entry.ProposedSubClass=propsubclass;
    entry.ProposedArrivalTime=proparrivaltime;
    entry.ProposedDepartureTime=propdeparturetime;

    let oids=[];                                        //Repeating for original flight schedule
    let oproparrivaltime=[];
    let opropdeparturetime=[];
    hops=data[key].Original.length;
    for (let i=0;i<hops;i++)
    {
      oids.push(data[key].Original[i][0]);
    }
    let opropclass=[];
    for (let i=0;i<hops;i++)
    {
      opropclass.push(data[key].Original[i][1]);
    }
    let opropsubclass=[];
    for (let i=0;i<hops;i++)
    {
      opropsubclass.push(data[key].Original[i][2]);
      if (i!=hops-1)
      {
        opropsubclass.push("#");
     }
    }
    for (let i=0;i<hops;i++)
    {
      oproparrivaltime.push(data[key].Original[i][3]);
      opropdeparturetime.push(data[key].Original[i][4]);
    }
    
    entry.OriginalID=oids;
    entry.OriginalClass=opropclass;
    entry.OriginalSubClass=opropsubclass;
    entry.OriginalArrivalTime=oproparrivaltime;
    entry.OriginalDepartureTime=opropdeparturetime;


    return {                                                                 
      PNR_Number: key,                                
      ProposedArrivalTime: entry.ProposedArrivalTime,
      ProposedDepartureTime: entry.ProposedDepartureTime,
      OriginalArrivalTime: entry.OriginalArrivalTime,
      OriginalDepartureTime: entry.OriginalDepartureTime,
      Flight: `Flight('Inventory ID: ${entry.ProposedID}, Departure City: ${entry.ProposedClass}, Arrival City: ${entry.ProposedSubClass})`,
      CancelledFlight: `Flight('Inventory ID: ${entry.OriginalID}, Departure City: ${entry.OriginalClass}, Arrival City: ${entry.OriginalSubClass})`,
    };
  });
  return entries;
};



const shuffleArray = (array) => {                         //Randomly arrange PNRs 
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  if (array.length>24)            
  {
    return array.slice(0,27);                             //If more than 27 PNRs present, return only first 27
  }
  else
  {
    return array;
  }
  
};

const App = () => {                                                 //State variables
  const [highlightFile, sethighlightFile] = useState(true);
  const [shuffledFile, setShuffledFile] = useState([]);
  const [selectedPNR, setSelectedPNR] = useState(null);
  const [selectedInfo, setSelectedInfo] = useState(null);
  const [selectedCancelledInfo, setSelectedCancelledInfo] = useState(null);
  
  
  
  const move = () => {                                        //To move passenger icon when PNRs are pressed
    document.getElementById('mover').style.display="flex";    //Make icon visible
    //Move to right side after small delay
    setTimeout(() => { document.getElementById('mover').style.transform="translate(1040px)"; }, 50);
    //Make icon disappear again
    setTimeout(() => {try{document.getElementById('mover').style.display="none";}
    catch{}
    //Make disappeared icon move back to left
    setTimeout(() => { try{document.getElementById('mover').style.transform="translate(250px)";}  catch{}}
    , 50);
  }, 3000);
      };

  useEffect(() => {
    const convertedFile = convertNewFormat(file);            //JSON file 
    setShuffledFile(shuffleArray([...convertedFile]));        //Shuffle PNRs
  }, [highlightFile]);

  const handleCardClick = (entry) => {                       //To show animation on click of PNR card
    try{
      setSelectedPNR((entry.PNR_Number).replace(/\#.*/,''));  //Remove # from PNR numbers
      //fetch information
      const flightInfo = entry.Flight.match(/Inventory ID: (\S+), Departure City: (\S+), Arrival City: (\S+)/);
      if (flightInfo) {
        const [, inventoryId, departureCity, arrivalCity] = flightInfo;   //Split into variable
        let string="";                                                    //String to hold all information of PNR
        const ID = inventoryId.split(",");                                //Get respective lists
        const cabin=departureCity.split(",");
        const classs=arrivalCity.split(",");
  
        const fixed_class=[];                                            //To handle multiple PAX having different classes
        let j=0;
        for (let i=0;i<classs.length;i++)
        {
          if (classs[i]!='#')
          {
            fixed_class[j]=classs[i];
          }
          else
          {
            j++;
            fixed_class[j]=classs[i];
          }
        }                                               

        for (let i=0;i<ID.length;i++)             //Adding information to string
        { 
          if (ID.length!=1)
          {
          string+='Flight ';
          string+=i+1;
          string+=':\n';
          }
          string+='Inventory ID: '+ID[i]+'\n';
          string+='Cabin       : '+cabin[i]+'\n';
          if (fixed_class[i][fixed_class[i].length-1]==')')
          {
            fixed_class[i] = fixed_class[i].slice(0, -1);
          }
          string+='Class       : '+fixed_class[i]+'\n';                       //formatting to make all colums equally spaced
          string+='Arrival     : '+entry.ProposedArrivalTime+'\n';
          string+='Departure   : '+entry.ProposedDepartureTime+'\n';
          string+='\n'; 
        }
        setSelectedInfo(`${string}`);       //display the string
      }

      // Extracting information from the Cancelled Flights attribute
      //repeating above steps for cancelled flight schedule
      const cancelledflightInfo = entry.CancelledFlight.match(/Inventory ID: (\S+), Departure City: (\S+), Arrival City: (\S+)/);
      if (cancelledflightInfo) 
        {
        const [, cancelledinventoryId, cancelledDepartureCity, cancelledArrivalCity] = cancelledflightInfo;
        let string2="";
        const ID2 = cancelledinventoryId.split(",");
        const cabin2=cancelledDepartureCity.split(",");
        const classs2=cancelledArrivalCity.split(",");
        const fixed_class2=[];
        let j=0;
        for (let i=0;i<classs2.length;i++)
        {
          if (classs2[i]!='#')
          {
            fixed_class2[j]=classs2[i];
          }
          else
          {
            j++;
            fixed_class2[j]=classs2[i];
          }
        }

        for (let i=0;i<ID2.length;i++)
        { 
          if (ID2.length!=1)
          {
          string2+='Flight ';
          string2+=i+1;
          string2+=':\n';
          }
          string2+='Inventory ID: '+ID2[i]+'\n';
          string2+='Cabin       : '+cabin2[i]+'\n';
          if (fixed_class2[i][fixed_class2[i].length-1]==')')
          {
            fixed_class2[i] = fixed_class2[i].slice(0, -1);
          }
          string2+='Class       : '+fixed_class2[i]+'\n';
          string2+='Arrival     : '+entry.OriginalArrivalTime+'\n';
          string2+='Departure   : '+entry.OriginalDepartureTime+'\n';
          string2+='\n'; 
        }
        setSelectedCancelledInfo(`${string2}`);

      }

    
    //Call function that moves passenger icon after rendering flight schedules
    move();
    
  }
  catch{}
  };

  const getFileClass = () => (highlightFile ? 'red clickable' : '');
  

  //HTML 
  return (
    <div>
      <div id="heading">
      <h1>FLIGHT SCHEDULE CHANGES</h1>
      <p id="subhead">CLICK ON THE AFFECTED PNR TO VIEW THE UPDATED FLIGHT SCHEDULE</p>
      </div>
      <div className="card-container">
        {/*Fetch PNR numbers and display */}
        {shuffledFile.map((entry, index) => (
          <div
            key={index}
            className={`card ${getFileClass()}`}
            onClick={() => handleCardClick(entry)
            
            }
          >
            {/*Replace # in PNR*/}
            <p>{(entry.PNR_Number).replace(/\#.*/,'')}</p>
          </div>
        ))}
      </div>
      <p></p>
      <p></p>
      <div className="textbox-container1">
      {highlightFile && selectedPNR && (
          <div className="textbox smaller" id = "mover">
          <img src = {icon}></img>
          
            <input type="text" id="qwerty" value={selectedPNR} readOnly />
          </div>
        )}
      </div>
      <div className="textbox-container">
        {highlightFile && selectedCancelledInfo && (
          <div className="textbox rounded" id="left" style={{alignItems: "center"}}>
          <div className="Head"><p id="flightHead"> Original Flight</p></div>
          <img src={plane} id="leftplane"></img>
          <div className="Info"><p id="content">{selectedCancelledInfo}</p></div>
          </div>
        )}

        {highlightFile && selectedInfo && (
          <div className="textbox rounded" id = "right" style={{alignItems: "center"}}>
          <div className="Head" style={{width:"300px"}}><p style={{textAlign:"center"}} id="flightHead">New Flight</p></div>
          <img src={plane} id="rightplane"></img>
          <div className="Info"><p id="content">{selectedInfo}</p></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
