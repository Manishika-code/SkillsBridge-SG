import '../Pages/Compare.css';
import { Link } from "react-router-dom";

export default function Compare(){

    return (
        <div id='compareContainer'>
            <div>
                <h1>Compare Results</h1>
            </div>

            <div>
                <Link to="/dashboardPage"><button>Back</button></Link>
            </div>
        </div>
    )
}