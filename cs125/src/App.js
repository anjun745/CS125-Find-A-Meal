import './App.css';
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
//import Home from "./pages/Home";
import PersonalInfo from "./pages/PersonalInfo";
import Search from "./pages/Search";
import Home from "./pages/Home"

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <nav className="navbar">
            <ul>
              <li><Link to='/'>Home</Link></li>
              <li><Link to='/personal'>Personal Info</Link></li>
              <li><Link to='/search'>Search</Link></li>
            </ul>
          </nav>
        </header>

        <Routes>
          <Route path="/" element={<Home/>}/>
          <Route path="/personal" element={<PersonalInfo/>}/>
          <Route path="/search" element={<Search/>}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
