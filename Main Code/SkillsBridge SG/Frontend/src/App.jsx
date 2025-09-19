import './App.css';
import { Routes, Route} from 'react-router-dom';
import Home from './Pages/Home.jsx';
import Dashboard from './Pages/Dashboard.jsx';
import Login from './Pages/Login.jsx';
import Category from './Pages/Category.jsx';
import Compare from './Pages/Compare.jsx';

export default function App() {
  // Define all routing paths
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboardPage" element={<Dashboard/>} />
        <Route path="/loginPage" element={<Login/>} />
        <Route path="/categoryPage" element={<Category/>} />
        <Route path="/comparePage" element={<Compare/>} />
      </Routes>     
    </>
  )
}