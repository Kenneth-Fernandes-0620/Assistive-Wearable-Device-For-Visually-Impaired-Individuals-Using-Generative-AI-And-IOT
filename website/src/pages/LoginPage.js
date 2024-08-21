import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errors, setErrors] = useState({});
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        const validationErrors = {};

        if (!email) {
            validationErrors.email = 'Email is required';
        } else if (!/\S+@\S+\.\S+/.test(email)) {
            validationErrors.email = 'Email is invalid';
        }

        if (!password) {
            validationErrors.password = 'Password is required';
        } else if (password.length < 6) {
            validationErrors.password = 'Password must be at least 6 characters';
        }

        if (Object.keys(validationErrors).length === 0) {
            console.log('Form submitted:', { email, password });
        } else {
            setErrors(validationErrors);
        }
    };

    const goBack = () => {
        navigate('/dashboard');
    };

    return (
        <div className="login-container">
            <button onClick={goBack} className="back-button">Back to Dashboard</button>
            <div className="login-form">
                <h1>Login</h1>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="email">Email:</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                        {errors.email && <p className="error">{errors.email}</p>}
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Password:</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        {errors.password && <p className="error">{errors.password}</p>}
                    </div>
                    <button type="submit" className="submit-button">Login</button>
                </form>
            </div>
            <style jsx>{`
                .login-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    font-family: 'Arial', sans-serif;
                    background-color: #f0f2f5;
                }
                .login-form {
                    background-color: white;
                    padding: 2rem;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    width: 100%;
                    max-width: 400px;
                }
                h1 {
                    color: #1877f2;
                    text-align: center;
                    margin-bottom: 1.5rem;
                }
                .form-group {
                    margin-bottom: 1rem;
                }
                label {
                    display: block;
                    margin-bottom: 0.5rem;
                    color: #444;
                }
                input {
                    width: 100%;
                    padding: 0.5rem;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-size: 1rem;
                }
                .error {
                    color: #d32f2f;
                    font-size: 0.875rem;
                    margin-top: 0.25rem;
                }
                .submit-button {
                    width: 100%;
                    padding: 0.75rem;
                    background-color: #1877f2;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 1rem;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                .submit-button:hover {
                    background-color: #166fe5;
                }
                .back-button {
                    position: absolute;
                    top: 1rem;
                    left: 1rem;
                    padding: 0.5rem 1rem;
                    background-color: #f0f2f5;
                    color: #1877f2;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                .back-button:hover {
                    background-color: #e4e6eb;
                }
            `}</style>
        </div>
    );
}

export default LoginPage;