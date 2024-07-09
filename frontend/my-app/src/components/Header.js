import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="header">
      <span className="title">Gomoku</span>
      <div className="buttons">
        <Link to="/"><button>Play</button></Link>
        <Link to="/about"><button>About</button></Link>
        <Link to="/players"><button>Players</button></Link>
        <Link to="/account"><button>Account</button></Link>
      </div>
    </header>
  );
}

export default Header;
