import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function UserDashboard() {
    const navigate = useNavigate();

    const handleLogout = () => {
        // Implement logout logic here
        navigate('/login');
    };

    return (
        <div className="dashboard-container">
            <div className="dashboard-header">
                <h1>Name</h1>
                <div className="header-buttons">
                    <Link to="/" className="header-button">Home</Link>
                    <button className="header-button" onClick={handleLogout}>Logout</button>
                </div>
            </div>
            <div className="dashboard-content">
                <div className="user-info">
                    <p>Age</p>
                    <p>Email</p>
                    <p>Location</p>
                    <p>Queries</p>
                </div>
                <div className="charts-container">
                    <div className="chart-box">
                        <h2>Location Based</h2>
                        <div className="chart">Chart</div>
                    </div>
                    <div className="chart-box">
                        <h2>Word Frequency</h2>
                        <div className="chart">Chart</div>
                    </div>
                    <div className="chart-box">
                        <h2>Query Frequency</h2>
                        <div className="chart">Chart</div>
                    </div>
                </div>
            </div>
            <style jsx>{`
                .dashboard-container {
                    font-family: 'Arial', sans-serif;
                    background-color: #f0f2f5;
                    min-height: 100vh;
                    padding: 20px;
                    color: #1c1e21;
                }
                .dashboard-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                }
                h1 {
                    color: #1877f2;
                    margin: 0;
                }
                .header-buttons {
                    display: flex;
                    gap: 10px;
                }
                .header-button {
                    background-color: #1877f2;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                .header-button:hover {
                    background-color: #166fe5;
                }
                .dashboard-content {
                    display: flex;
                    gap: 20px;
                }
                .user-info {
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    flex: 1;
                }
                .charts-container {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 20px;
                    flex: 3;
                }
                .chart-box {
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    flex: 1 1 calc(33.333% - 20px);
                    min-width: 250px;
                }
                h2 {
                    color: #1877f2;
                    margin-top: 0;
                }
                .chart {
                    height: 200px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
            `}</style>
        </div>
    );
}

export default UserDashboard;
