import '../Pages/Login.css';
import { Link } from "react-router-dom";

export default function Login() {
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
                        Username or E-mail
                    </label>
                    <input
                        type="text"
                        id="username"
                        className="login-input"
                    />
                    <label className="login-label" htmlFor="password">
                        Password
                    </label>
                    <input
                        type="password"
                        id="password"
                        className="login-input"
                    />
                    <Link to="/categoryPage">
                        <button type="button" className="login-button">
                            Log in
                        </button>
                    </Link>
                </form>
            </div>
        </div>
    );
}
