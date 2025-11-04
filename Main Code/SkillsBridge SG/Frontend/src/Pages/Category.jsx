import '../Pages/Category.css';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import Skill from '../Components/Skill';
import BackBar from '../Components/BackBar';
import { useEffect, useState } from 'react';

const API_BASE = "http://localhost:8000/api";


export default function Category() {
    const [skills, setSkills] = useState([]);
    const [selectedSkills, setSelectedSkills] = useState([]);
    const [level, setLevel] = useState(null);
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();

    const source = searchParams.get('source');

    console.log(source);

    useEffect(() => {
        fetch(`${API_BASE}/skills/`)
            .then(res => res.json())
            .then(data => {
                const mapped = data.map(s => ({
                    id: s.id,
                    name: s.name,
                    icon: assignIcon(s.name)
                }));
                setSkills(mapped);
            })
            .catch(err => console.error("Error fetching skills:", err));
    }, []);

    const assignIcon = (skillName) => {
        if (skillName.toLowerCase().includes("code")) return "⌨️";
        if (skillName.toLowerCase().includes("design")) return "🎨";
        if (skillName.toLowerCase().includes("science")) return "🧪";
        if (skillName.toLowerCase().includes("math")) return "➗";
        return "📘"; // fallback icon
    };

    const toggleSkill = (skillName) => {
        setSelectedSkills(prev => 
            prev.includes(skillName) 
            ? prev.filter(s => s !== skillName) 
            : [...prev, skillName]
        );
    };

    // validation check to ensure all necessary buttons are clicked
    const handleConfirm = () => {
        if (selectedSkills.length === 0) {
            alert("Please select at least one skill!");
            return;
        }
        else if(level === null)
        {
            alert("Please select either Degree or Diploma!");
            return;
        }       

        localStorage.setItem("selectedSkills", JSON.stringify(selectedSkills));
        localStorage.setItem("selectedLevel", level);
        navigate(`/dashboardPage?skills=${selectedSkills.join(",")}&level=${level}&source=${source}`);
    };

    return (
        <div id="categoryPage">
            <BackBar to="/" />

            <div id="categoryPageWrapper">
                <h1 id="categoryTitle">Select your skills</h1>

                <div id="skillGrid">
                    {skills.map((s) =>
                        <Skill 
                            key={s.id} 
                            icon={s.icon} 
                            skillName={s.name}
                            onClick={() => toggleSkill(s.name)}
                            isSelected={selectedSkills.includes(s.name)}
                        />
                    )}
                </div>

                <div id="degreeSelector">
                    <button 
                        className={`degreeBtn ${level === "uni" ? "active" : ""}`} 
                        onClick={() => setLevel("uni")}
                    >
                        Degree
                    </button>
                    <button 
                        className={`degreeBtn ${level === "poly" ? "active" : ""}`} 
                        onClick={() => setLevel("poly")}
                    >
                        Diploma
                    </button>
                </div>

                <button onClick={handleConfirm}>Confirm</button>
            </div>
        </div>
    );
}

