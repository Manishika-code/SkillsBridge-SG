import '../Pages/Login.css';
import { Link } from "react-router-dom";

export default function Login(){

    return (
        <div id='loginContainer'>
            <div>
                <h1>Login</h1>
            </div>

            <div>
                <Link to="/"><button>Back</button></Link>
                <Link to="/categoryPage"><button>Confirm</button></Link>
            </div>
        </div>
    )
}