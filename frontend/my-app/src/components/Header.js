import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Header() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  return (
    <header className="header">
      <span className="title">Gomoku</span>
      <div className="buttons">
        <Link to="/"><button>Play</button></Link>
        <Link to="/about"><button>About</button></Link>
        <Link to="/lobbies"><button>Lobbies</button></Link>
        <Link to="/players"><button>Players</button></Link>
        <Link to="/friends"><button>Friends</button></Link>
        <Link to="/account"><button>Account</button></Link>
        
        {localStorage.getItem("token") && <button onClick={handleLogout}>Logout</button>}
      </div>
    </header>
  );
}

export default Header;