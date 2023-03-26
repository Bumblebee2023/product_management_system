import React from 'react'
import Chart from "./components/Chart";
import './styles/index.css';
import Navbar from "./components/Navbar/Navbar";
import FileReader from "./components/FileReader/FileReader";

const App = () => {
  return (
    <div className='app'>
      <Navbar />
      <section className='main'>
        <div className='container'>
          <FileReader />
          <Chart />
        </div>
      </section>
    </div>
  );
};

export default App
