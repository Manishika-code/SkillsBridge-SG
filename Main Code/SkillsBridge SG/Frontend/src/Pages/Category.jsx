import '../Pages/Category.css';
import { Link } from 'react-router-dom';
import Skill from '../Components/Skill';
import BackBar from '../Components/BackBar';


const skillData = [
    { icon: "⌨️", skillName: "Coding" },
    { icon: "🎨", skillName: "Design" },
    { icon: "🧪", skillName: "Science" },
    { icon: "➗", skillName: "Mathematics" },
    { icon: "✏️", skillName: "Graphic Design" },
    { icon: "✒️", skillName: "Creative Writing" },
    { icon: "📈", skillName: "Economics" },
    { icon: "⏻", skillName: "Electronics" }
];

export default function Category() {
    return (
        <div id="categoryPage">
            
            <BackBar to="/"/>

            <div id="categoryPageWrapper">
                <h1 id="categoryTitle">Select your skills</h1>
                <div id="skillGrid">
                    {skillData.map((d, idx) =>
                        <Skill key={d.skillName} icon={d.icon} skillName={d.skillName} />
                    )}
                </div>
                <div id="degreeSelector">
                    <button className="degreeBtn">Degree</button>
                    <button className="degreeBtn">Diploma</button>
                </div>
                    <Link to="/dashboardPage"><button>Confirm</button></Link>
            </div>
        </div>
    );
}
