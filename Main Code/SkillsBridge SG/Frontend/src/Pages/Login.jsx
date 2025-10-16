import '../Pages/Login.css';
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();

    const handleUsernameChange = (e) => {
        setUsername(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const isFormValid = username.trim() !== '' && password.trim() !== '';

    const handleLogin = () => {
        if (isFormValid) {
            navigate('/categoryPage');
        }
    };

    return (
        <div className="login-page">
            <div className="back-bar">
                <Link to="/" className="back-link">
                    <span className="back-arrow">&#8592;</span>
                    <span className="back-text">BACK</span>
                </Link>
            </div>
            <div className="login-container">
                <h1 className="login-title">Log in</h1>
                <form className="login-form">
                    <label className="login-label" htmlFor="username">
                        Username
                    </label>
                    <input
                        type="text"
                        id="username"
                        className="login-input"
                        value={username}
                        onChange={handleUsernameChange}
                    />
                    <label className="login-label" htmlFor="password">
                        Password
                    </label>
                    <div className="password-input-container">
                        <input
                            type={showPassword ? "text" : "password"}
                            id="password"
                            className="login-input password-input"
                            value={password}
                            onChange={handlePasswordChange}
                        />
                        <span 
                            className="password-toggle-icon"
                            onClick={() => setShowPassword(!showPassword)}
                        >
                            {showPassword ? '👁️' : '👁️‍🗨️'}
                        </span>
                    </div>
                    <button 
                        type="button" 
                        className="login-button" 
                        disabled={!isFormValid}
                        onClick={handleLogin}
                    >
                        Log in
                    </button>

                    <p className="signup-text">
                        Don't have an account? <Link to="/registerPage">Sign up</Link>
                    </p>
                </form>
            </div>
        </div>
    );
}
