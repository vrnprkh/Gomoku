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
import DetailedMoves from './components/DetailedMoves';
import SelfLobbies from './components/SelfLobbies';

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
          <Route path="/viewgame/:gid" element={<DetailedMoves />} />
          <Route path="/self-lobbies" element={<SelfLobbies />}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;