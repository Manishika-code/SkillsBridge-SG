import '../Pages/Category.css';
import { Link } from "react-router-dom";

export default function Category(){

    return (
        <div id='categoryContainer'>
            <div>
                <h1>Select your skills</h1>
            </div>

            <div>
                <Link to="/"><button>Back</button></Link>
                <Link to="/dashboardPage"><button>Confirm</button></Link>
            </div>
        </div>
    )
}