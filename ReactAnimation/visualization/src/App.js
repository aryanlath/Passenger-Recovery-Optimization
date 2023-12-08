// App.js
  
import React, { useState, useEffect } from 'react';
import file1 from './file1.json';
import file2 from './file2.json';
import './styles.css'; // Import the CSS file
import icon from './icon2.jpeg'
import plane from './plane.png'


const shuffleArray = (array) => {
  // Fisher-Yates (Knuth) shuffle algorithm
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
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
    setShuffledFile1(shuffleArray([...file1]));
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
        setSelectedInfo(`NEW FLIGHT\n\n${inventoryId}\n${departureCity}\n${arrivalCity}`);
      }

      // Extracting information from the Cancelled Flights attribute
      const cancelledFlightInfo = entry['Cancelled Flights'].match(/Inventory ID: (\S+), Departure City: (\S+), Arrival City: (\S+)/);
      if (cancelledFlightInfo) {
        const [, cancelledInventoryId, cancelledDepartureCity, cancelledArrivalCity] = cancelledFlightInfo;
        setSelectedCancelledInfo(`CANCELLED FLIGHT\n\n${cancelledInventoryId}\n${cancelledDepartureCity}\n${cancelledArrivalCity}`);
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
