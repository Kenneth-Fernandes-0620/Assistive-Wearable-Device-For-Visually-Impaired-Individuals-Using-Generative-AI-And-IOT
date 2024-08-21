import logo from './logo.svg';
import './App.css';
import DashboardPage from './pages/DashboardPage';
import LoginPage from './pages/LoginPage';
import UserDashboard from './pages/UserDashboard';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/dashboard" element={<UserDashboard />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
