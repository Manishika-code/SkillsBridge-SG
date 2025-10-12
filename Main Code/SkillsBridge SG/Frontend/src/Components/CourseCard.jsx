import '../Components/CourseCard.css';

const CourseCard = ({qualific,
                    courseName,
                    institution,
                    schoolCtg,
                    courseDesr,
                    courseType,
                    onCardClick, 
                    isChecked,        // Check if checkbox is checked
                    onCheckboxChange, // Handle checkbox changes
                    isSelected,
                    hasSelection,
                    showToggleUI}) => {
    return (
        <div id="cardContainer">            
            <div className='cardContent'>

                <div className={`${hasSelection ? (isSelected ? 'selected' : 'unselected'): 'default'}`}>

                    {showToggleUI && (
                        <div className='checkbox'>
                            <input type="checkbox" checked={isChecked} onChange={(e) => onCheckboxChange(e.target.checked)}/>
                        </div>
                    )}

                    <h3>{qualific}</h3>
                    <h1>{courseName}</h1>
                    
                    <hr></hr>

                    <p className='sub-desc'>{institution} {schoolCtg && `| ${schoolCtg}`}</p>

                    <div className='desc'>
                        <p>{courseDesr}</p>
                    </div>

                    <div className='cardbottom'> 
                        <div className='courseType'>{courseType}</div>
                        <button onClick={onCardClick} disabled={hasSelection}>Show More</button>
                    </div>

                </div>

            </div>
        </div>
    );
}
export default CourseCard;