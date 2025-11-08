import '../Pages/Register.css';
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useState } from "react";
import BackBar from '../Components/BackBar';

export default function Register() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const [searchParams] = useSearchParams();
    const source = searchParams.get('source');

    const isFormValid =
        username.trim() !== '' &&
        password.trim() !== '' &&
        confirmPassword.trim() !== '';

    const handleSignUp = async (e) => {
        e.preventDefault();
        setError('');

        if (!isFormValid) return;
        if (password !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        setLoading(true);

        try {
            const response = await fetch("http://127.0.0.1:8000/api/auth/register/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    role: "student" 
                }),
            });

            if (response.ok) {
                // success
                const data = await response.json();
                console.log("Registered:", data);
                alert("Registration successful! Please log in.");
                navigate(`/loginPage?source=${source}`);
            } else {
                // failed validation
                const errorData = await response.json();
                console.error("Error response:", errorData);
                if (errorData.username) {
                    setError("Username already exists");
                } else if (errorData.password) {
                    setError("Password is too short or invalid");
                } else {
                    setError("Registration failed. Please check your details.");
                }
            }
        } catch (err) {
            console.error("Error:", err);
            setError("Server error. Please try again later.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="register-page">
            
            <BackBar to={`/loginPage?source=${source}`}/>

            <div className="register-container">
                <h1 className="register-title">REGISTER</h1>

                <form className="register-form" onSubmit={handleSignUp}>
                    <label className="register-label" htmlFor="username">Username</label>
                    <input
                        type="text"
                        id="username"
                        className="register-input"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />

                    <label className="register-label" htmlFor="password">Password</label>
                    <div className="password-input-container">
                        <input
                            type={showPassword ? "text" : "password"}
                            id="password"
                            className="register-input password-input"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <span
                            className="password-toggle-icon"
                            onClick={() => setShowPassword(!showPassword)}
                        >
                            {showPassword ? '👁️' : '👁️‍🗨️'}
                        </span>
                    </div>

                    <label className="register-label" htmlFor="confirmPassword">Confirm Password</label>
                    <div className="password-input-container">
                        <input
                            type={showConfirmPassword ? "text" : "password"}
                            id="confirmPassword"
                            className="register-input password-input"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                        />
                        <span
                            className="password-toggle-icon"
                            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        >
                            {showConfirmPassword ? '👁️' : '👁️‍🗨️'}
                        </span>
                    </div>

                    {error && <p className="error-text">{error}.</p>}

                    <button
                        type="submit"
                        className="register-button"
                        disabled={!isFormValid || loading}
                    >
                        {loading ? "Signing Up..." : "Sign Up"}
                    </button>
                </form>
            </div>
        </div>
    );
}
