import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Gameboard from './components/Gameboard';
import Header from './components/Header';
import About from './components/About';
import Account from './components/Account';

function App() {
  return (
    <Router>
      <div>
        <Header />
        <Routes>
          <Route path="/" element={<Gameboard />} />
          <Route path="/about" element={<About />} />
          <Route path="/account" element={<Account />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
