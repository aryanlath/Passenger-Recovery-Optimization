// App.js
import result from './result (1).json'
import React, { useState, useEffect } from 'react';
import file1 from './file1.json';
import file2 from './file2.json';
import './styles.css'; // Import the CSS file
import icon from './icon2.jpeg'
import plane from './plane.png'

const convertNewFormat = (data) => {
  const entries = Object.keys(data).map((key) => {
    const entry = data[key];


    let ids=[];
    let hops=data[key].Proposed.length;
    for (let i=0;i<hops;i++)
    {
      ids.push(data[key].Proposed[i][0]);
    }
    let propclass=[];
    for (let i=0;i<hops;i++)
    {
      propclass.push(data[key].Proposed[i][1]);
    }
    let propsubclass=[];
    for (let i=0;i<hops;i++)
    {
      propsubclass.push(data[key].Proposed[i][2]);
      if (i!=hops-1)
      {
        propsubclass.push("#");
     }
    }

    

    entry.ProposedID=ids;
    entry.ProposedClass=propclass;
    entry.ProposedSubClass=propsubclass;

    let oids=[];
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
    
    entry.OriginalID=oids;
    entry.OriginalClass=opropclass;
    entry.OriginalSubClass=opropsubclass;


    return {
      PNR_Number: key,
      Cabin: entry.Proposed[0][1],
      Class: entry.Proposed[0][2][0],
      
      Flight: `Flight('Inventory ID: ${entry.ProposedID}, Departure City: ${entry.ProposedClass}, Arrival City: ${entry.ProposedSubClass})`,

      CancelledFlight: `Flight('Inventory ID: ${entry.OriginalID}, Departure City: ${entry.OriginalClass}, Arrival City: ${entry.OriginalSubClass})`,
    };
  });

  return entries;
};

const shuffleArray = (array) => {
  // Fisher-Yates (Knuth) shuffle algorithm
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array.slice(0,24);
};

const App = () => {
  const [highlightFile1, setHighlightFile1] = useState(false);
  const [highlightFile2, setHighlightFile2] = useState(false);
  const [shuffledFile1, setShuffledFile1] = useState([]);
  const [shuffledFile2, setShuffledFile2] = useState([]);
  const [selectedPNR, setSelectedPNR] = useState(null);
  const [selectedCabin, setSelectedCabin] = useState(null);
  const [selectedClass, setSelectedClass] = useState(null);
  const [selectedInfo, setSelectedInfo] = useState(null);
  const [selectedCancelledInfo, setSelectedCancelledInfo] = useState(null);
  const [showAllPNRs, setShowAllPNRs] = useState(false);
  
  
  
  const move = () => {  
    document.getElementById('mover').style.display="flex";
    setTimeout(() => { document.getElementById('mover').style.transform="translate(1040px)"; }, 50);
    setTimeout(() => {try{document.getElementById('mover').style.display="none";}
    catch{}
    setTimeout(() => { try{document.getElementById('mover').style.transform="translate(200px)";}  catch{}}
    , 50);
  }, 3000);
      };

  useEffect(() => {
    const convertedFile2 = convertNewFormat(result);
    //setShuffledFile1(shuffleArray([...file1]));
    setShuffledFile1(shuffleArray([...convertedFile2]));
    setShuffledFile2(shuffleArray([...file2]));
  }, [highlightFile1, highlightFile2]);

  const handleButtonClick = () => {
    if (showAllPNRs) {
      setHighlightFile1(false);
      setHighlightFile2(false);
      setShowAllPNRs(false);
    } else {
      setHighlightFile1(true);
      setHighlightFile2(true);
      setShowAllPNRs(true);
    }
  };

  const handleCardClick = (entry) => {
    try{
    // Only handle click for red cards
    if (highlightFile1) {
      setSelectedPNR(entry.PNR_Number);
      setSelectedCabin(entry.Cabin);
      setSelectedClass(entry.Class);

      // Extracting information from the Flight attribute
      const flightInfo = entry.Flight.match(/Inventory ID: (\S+), Departure City: (\S+), Arrival City: (\S+)/);
      if (flightInfo) {
        const [, inventoryId, departureCity, arrivalCity] = flightInfo;
        let string="NEW FLIGHT\n\n";
        const ID = inventoryId.split(",");
        const cabin=departureCity.split(",");
        const classs=arrivalCity.split(",");
        const fixed_class=[];
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
        for (let i=0;i<ID.length;i++)
        { 
          if (ID.length!=1)
          {
          string+='Flight ';
          string+=i+1;
          string+=':\n';
          }
          string+=ID[i]+'\n';
          string+=cabin[i]+'\n';
          if (fixed_class[i][fixed_class[i].length-1]==')')
          {
            fixed_class[i] = fixed_class[i].slice(0, -1);
          }
          string+=fixed_class[i]+'\n';
          string+='\n'; 
        }
        setSelectedInfo(`${string}`);
      }

      // Extracting information from the Cancelled Flights attribute
      const cancelledflightInfo = entry.CancelledFlight.match(/Inventory ID: (\S+), Departure City: (\S+), Arrival City: (\S+)/);
      if (cancelledflightInfo) 
        {
          console.log(cancelledflightInfo);
        const [, cancelledinventoryId, cancelledDepartureCity, cancelledArrivalCity] = cancelledflightInfo;
        let string2="ORIGINAL FLIGHT\n\n";
        const ID2 = cancelledinventoryId.split(",");
        const cabin2=cancelledDepartureCity.split(",");
        const classs2=cancelledArrivalCity.split(",");
        console.log(ID2);
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
        //console.log(ID2);
        for (let i=0;i<ID2.length;i++)
        { 
          if (ID2.length!=1)
          {
          string2+='Flight ';
          string2+=i+1;
          string2+=':\n';
          }
          string2+=ID2[i]+'\n';
          string2+=cabin2[i]+'\n';
          if (fixed_class2[i][fixed_class2[i].length-1]==')')
          {
            fixed_class2[i] = fixed_class2[i].slice(0, -1);
          }
          string2+=fixed_class2[i]+'\n';
          string2+='\n'; 
        }
        setSelectedCancelledInfo(`${string2}`);

      }

    }

    move();
  }
  catch{}
  };

  const getFile1Class = () => (highlightFile1 ? 'red clickable' : '');
  const getFile2Class = () => (highlightFile2 ? 'green' : '');


  return (
    <div>
      <div id="heading">
      <h1>PNR Numbers</h1>
      </div>
      <div className="card-container">
        {shuffledFile1.map((entry, index) => (
          <div
            key={index}
            className={`card ${getFile1Class()}`}
            onClick={() => handleCardClick(entry)
            
            }
          >
            <p>{entry.PNR_Number}</p>
          </div>
        ))}
        {shuffledFile2.map((entry, index) => (
          <div
            key={index}
            className={`card ${getFile2Class()}`}
            // Note: handleCardClick not applied to green cards
          >
            <p>{entry.PNR_Number}</p>
          </div>
        ))}
      </div>
      <div id="showpnr">
      <button onClick={handleButtonClick} id="pnrshower">{showAllPNRs ? 'Show all PNRs' : 'Show affected PNRs'}</button>
      </div>
      <p></p>
      <p></p>
      <div className="textbox-container1">
      {highlightFile1 && selectedPNR && (
          <div className="textbox smaller" id = "mover">
          <img src = {icon}></img>
          
            <input type="text" value={selectedPNR} readOnly />
          </div>
        )}
      </div>
      <div className="textbox-container">
        {highlightFile1 && selectedCancelledInfo && (
          <div className="textbox rounded">
          <img src={plane} className="plane" id="leftplane"></img>
            <textarea value={selectedCancelledInfo} readOnly />
          </div>
        )}

        {highlightFile1 && selectedInfo && (
          <div className="textbox rounded" id = "right" >
          <img src={plane} id="rightplane"></img>
            <textarea value={selectedInfo} readOnly />
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
