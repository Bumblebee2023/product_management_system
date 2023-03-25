import React from 'react'
import Chart from "./components/Chart";
import './styles/index.css';
import Navbar from "./components/Navbar/Navbar";

const App = () => {
  return (
    <div className='app'>
      <Navbar />
      <main className='main'>
        <div className='container'>
          <Chart />
        </div>
      </main>
    </div>
  );
};

export default App
