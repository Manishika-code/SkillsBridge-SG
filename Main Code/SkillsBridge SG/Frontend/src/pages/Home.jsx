import '../Pages/Home.css';
import { Link } from "react-router-dom";

export default function Home(){

    return (
        <div id='homeContainer'>
            <div id='homeHeader'>
                <h2>Skills Bridge SG</h2>
                <h1>Personalised Educational Roadmap</h1>
            </div>

            <div>
                <Link to="/dashboardPage"><button>Visitor</button></Link>
                <Link to="/loginPage"><button>Student</button></Link>
            </div>
        </div>
    );
}