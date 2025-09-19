import '../Components/CourseCard.css';

const CourseCard = (course) => {
    return (
        <div id="cardContainer">
            <div className='cardContent'>
                <h3>{course.qualific}</h3>
                <h1>{course.courseName}</h1>
                
                <hr></hr>

                <p className='sub-desc'>{course.institution} | {course.schoolCtg}</p>

                <p>{course.courseDesr}</p>

                <div className='cardbottom'> 
                    <div className='courseType'>{course.courseType}</div>
                    <button>Show More</button>
                </div>
            </div>
        </div>
    );
}
export default CourseCard;