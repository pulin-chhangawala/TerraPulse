import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [zipcode, setZipcode] = useState('');
  const [electricityUnits, setElectricityUnits] = useState('');
  const [gasUnits, setGasUnits] = useState('');
  const [peopleInHome, setPeopleInHome] = useState('');
  const [currentLocation, setCurrentLocation] = useState('');
  const [destination, setDestination] = useState('');
  const [result, setResult] = useState(null);
  const [transportResult, setTransportResult] = useState(null);
  const [error, setError] = useState('');

  const handleEmissionsSubmit = async (e) => {
      e.preventDefault();
      setError('');
      setResult(null);

      try {
          const response = await axios.post('http://localhost:5000/calculate_co2', {  // Adjust the URL as necessary
              zipcode,
              electricity_units: electricityUnits,
              gas_units: gasUnits,
              peopleInHome
          });
          setResult(response.data);
      } catch (err) {
          setError(err.response?.data?.error || 'An error occurred');
      }
  };

  const handleTransportSubmit = async (e) => {
      e.preventDefault();
      setError('');
      setTransportResult(null);

      try {
          const response = await axios.post('http://localhost:5000/calculate_transport_emissions', {
              current_location: currentLocation,
              destination
          });
          setTransportResult(response.data);
      } catch (err) {
          setError(err.response?.data?.error || 'An error occurred');
      }
  };

  return (
      <div>
          <h1>CO2 Emissions Calculator</h1>
          <form onSubmit={handleEmissionsSubmit}>
              <h2>Home Emissions</h2>
              <div>
                  <label>Zip Code:</label>
                  <input type="text" value={zipcode} onChange={(e) => setZipcode(e.target.value)} required />
              </div>
              <div>
                  <label>Electricity Units:</label>
                  <input type="number" value={electricityUnits} onChange={(e) => setElectricityUnits(e.target.value)} required />
              </div>
              <div>
                  <label>Gas Units:</label>
                  <input type="number" value={gasUnits} onChange={(e) => setGasUnits(e.target.value)} required />
              </div>
              <div>
                  <label>People in Home:</label>
                  <input type="number" value={peopleInHome} onChange={(e) => setPeopleInHome(e.target.value)} required min="1" max="11" />
              </div>
              <button type="submit">Calculate</button>
          </form>

          {error && <p style={{ color: 'red' }}>{error}</p>}
          {result && (
              <div>
                  <h2>Home Emissions Results:</h2>
                  <p>Total CO2 Emissions: {result['Total CO2 Emissions (tonnes)']}</p>
                  <p>CO2 from Electricity: {result['CO2 from Electricity (tonnes)']}</p>
                  <p>CO2 from Gas: {result['CO2 from Gas (tonnes)']}</p>
                  <p>Ideal Emissions: {result['Ideal Emissions (tonnes)']}</p>
                  <h3>Suggestions:</h3>
                  <ul>
                      {result.Suggestions.map((suggestion, index) => (
                          <li key={index}>{suggestion[0]} - {suggestion[1]}</li>
                      ))}
                  </ul>
              </div>
          )}

          <form onSubmit={handleTransportSubmit}>
              <h2>Transportation Emissions</h2>
              <div>
                  <label>Current Location:</label>
                  <input type="text" value={currentLocation} onChange={(e) => setCurrentLocation(e.target.value)} required />
              </div>
              <div>
                  <label>Destination:</label>
                  <input type="text" value={destination} onChange={(e) => setDestination(e.target.value)} required />
              </div>
              <button type="submit">Calculate Transport Emissions</button>
          </form>

          {transportResult && (
              <div>
                  <h2>Transportation Emissions Results:</h2>
                  <ul>
                      {transportResult.map((data, index) => (
                          <li key={index}>
                              Mode: {data.mode}, Emissions: {data.emissions.toFixed(2)} kg CO2
                          </li>
                      ))}
                  </ul>
              </div>
          )}
      </div>
  );
}

export default App;
