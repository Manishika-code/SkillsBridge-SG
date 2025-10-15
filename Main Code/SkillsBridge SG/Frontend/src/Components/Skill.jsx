import '../Components/Skill.css';

const Skill = ({ icon, skillName }) => {
    return (
        <div className="skillContainer">
            <div className="skillContent">
                <span className="skillIcon">{icon}</span>
                <h2 className="skillTitle">{skillName}</h2>
            </div>
        </div>
    );
};

export default Skill;
