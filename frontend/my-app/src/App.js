import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Gameboard from './components/Gameboard';
import Players from './components/Players';
import Friends from './components/Friends';
import Lobbies from './components/Lobbies';
import Header from './components/Header';
import About from './components/About';
import Account from './components/Account';
import Login from './components/Login';
import Signup from './components/Signup';

function App() {
  return (
    <Router>
      <div>
        <Header />
        <Routes>
          <Route path="/" element={<Gameboard />} />
          <Route path="/about" element={<About />} />
          <Route path="/players" element={<Players />} />
          <Route path="/friends" element={<Friends />} />
          <Route path="/lobbies" element={<Lobbies />} />
          <Route path="/account" element={<Account />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;