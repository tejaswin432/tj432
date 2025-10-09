import React, { useState } from 'react';
import './App.css';
import Screen1 from './components/Screen1';
import Screen2 from './components/Screen2';

function App() {
  const [screen, setScreen] = useState('s1');
  const [results, setResults] = useState(null);

  const handleAnalysisComplete = (data) => {
    setResults(data);
    setScreen('s2');
  };

  const handleCloseScreen2 = () => {
    setScreen('s1');
    setResults(null);
  };

  return (
    <div className="App">
      {screen === 's1' && <Screen1 onAnalysisComplete={handleAnalysisComplete} />}
      {screen === 's2' && <Screen2 results={results} onClose={handleCloseScreen2} />}
    </div>
  );
}

export default App;