import '../Pages/Category.css';
import { Link } from 'react-router-dom';
import Skill from '../Components/Skill';

const skillData = [
    { icon: "⌨️", skillName: "Coding" },
    { icon: "🎨", skillName: "Design" },
    { icon: "🧪", skillName: "Science" },
    { icon: "➗", skillName: "Mathematics" },
    { icon: "✏️", skillName: "Graphic Design" },
    { icon: "✒️", skillName: "Creative Writing" },
    { icon: "🔊", skillName: "Public Speaking" },
    { icon: "📈", skillName: "Economics" },
    { icon: "⏻", skillName: "Electronics" }
];

export default function Category() {
    return (
        <div id="categoryPageWrapper">
            <div id="categoryHeader">
                <Link to="/"><span id="backArrow">←</span> BACK</Link>
            </div>
            <h1 id="categoryTitle">What are your skills?</h1>
            <div id="skillGrid">
                {skillData.map((d, idx) =>
                    <Skill key={d.skillName} icon={d.icon} skillName={d.skillName} />
                )}
            </div>
            <div id="degreeSelector">
                <button className="degreeBtn activeDegree">Degree</button>
                <button className="degreeBtn">Diploma</button>
            </div>
                <Link to="/dashboardPage"><button>Confirm</button></Link>
        </div>
    );
}
