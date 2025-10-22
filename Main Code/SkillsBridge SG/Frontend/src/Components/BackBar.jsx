import '../Components/BackBar.css';
import { FiArrowLeftCircle } from "react-icons/fi";
import { Link } from "react-router-dom";

const BackBar = ({ to = "/"}) =>{

    return(
        <div id="defaultBackBar">
            <div>
                <Link to={to}><div className='backBtn'><FiArrowLeftCircle size={40} /></div></Link> {/* To be changed: Direct to different pages for different user */}                
            </div>
        </div>
    )
}
export default BackBar;