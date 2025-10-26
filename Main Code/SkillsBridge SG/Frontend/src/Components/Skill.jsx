import '../Components/Skill.css';

const Skill = ({ icon, skillName, onClick, isSelected }) => {
    return (
        <div 
            className={`skillContainer ${isSelected ? "selected" : ""}`}
            onClick={onClick}
        >
            <div className="skillContent">
                <span className="skillIcon">{icon}</span>
                <h2 className="skillTitle">{skillName}</h2>
            </div>
        </div>
    );
};

export default Skill;

