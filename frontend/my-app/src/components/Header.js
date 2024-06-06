import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="header">
      <Link to="/"><button>Play</button></Link>
      <Link to="/about"><button>About</button></Link>
      <Link to="/account"><button>Account</button></Link>
    </header>
  );
}

export default Header;
