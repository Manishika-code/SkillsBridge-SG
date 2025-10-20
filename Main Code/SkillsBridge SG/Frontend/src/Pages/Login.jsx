import '../Pages/Login.css';
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleUsernameChange = (e) => setUsername(e.target.value);
    const handlePasswordChange = (e) => setPassword(e.target.value);

    const isFormValid = username.trim() !== '' && password.trim() !== '';

    const handleLogin = async (e) => {
        e.preventDefault();
        if (!isFormValid) return;

        setLoading(true);
        setError('');

        try {
            // 1️⃣ Send credentials to Django backend
            const response = await fetch("http://127.0.0.1:8000/api/auth/login/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                const errData = await response.json();
                setError(errData.detail || "Invalid username or password");
                setLoading(false);
                return;
            }

            const data = await response.json();

            // 2️⃣ Save tokens in localStorage
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);

            // 3️⃣ Fetch current user info
            const userRes = await fetch("http://127.0.0.1:8000/api/auth/me/", {
                headers: {
                    "Authorization": `Bearer ${data.access}`
                }
            });

            if (userRes.ok) {
                const userData = await userRes.json();
                localStorage.setItem("user", JSON.stringify(userData));
            }

            // 4️⃣ Redirect to category page
            navigate("/categoryPage");

        } catch (err) {
            console.error("Login error:", err);
            setError("Something went wrong. Please try again later.");
        } finally {
            setLoading(false);
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

                <form className="login-form" onSubmit={handleLogin}>
                    <label className="login-label" htmlFor="username">Username</label>
                    <input
                        type="text"
                        id="username"
                        className="login-input"
                        value={username}
                        onChange={handleUsernameChange}
                        autoComplete="username"
                    />

                    <label className="login-label" htmlFor="password">Password</label>
                    <div className="password-input-container">
                        <input
                            type={showPassword ? "text" : "password"}
                            id="password"
                            className="login-input password-input"
                            value={password}
                            onChange={handlePasswordChange}
                            autoComplete="current-password"
                        />
                        <span
                            className="password-toggle-icon"
                            onClick={() => setShowPassword(!showPassword)}
                        >
                            {showPassword ? '👁️' : '👁️‍🗨️'}
                        </span>
                    </div>

                    {error && <p className="error-text">{error}</p>}

                    <button
                        type="submit"
                        className="login-button"
                        disabled={!isFormValid || loading}
                    >
                        {loading ? "Logging in..." : "Log in"}
                    </button>

                    <p className="signup-text">
                        Don’t have an account? <Link to="/registerPage">Sign up</Link>
                    </p>
                </form>
            </div>
        </div>
    );
}
