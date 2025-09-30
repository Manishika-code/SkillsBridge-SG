import '../Pages/Dashboard.css';
import { Link } from "react-router-dom";
import CourseCard from '../Components/CourseCard';
import { useEffect, useState } from 'react';

// Computed in frontend, probably should compute in backend instead?
function getQualific(level) {
  switch(level) {
    case "poly": return "Diploma";
    case "uni": return "Degree";
    case "jc": return "A-Level";
    default: return "";
  }
}
export default function Dashboard(){  
    {/* Define functionality / datasets */}
    const [courses, setCourses] = useState([]);
    useEffect(() => {
      fetch("http://localhost:8000/api/courses/")
      .then((res) => res.json())
      .then((data) => setCourses(data))
      .catch((err) => console.error("Error fetching courses:", err));
  }, []);

    


/*
   const populateCourseCards = [
        { id: 1, qualific:"Diploma in", courseName:"Accountancy", institution:"Ngee Ann Polytechnic", schoolCtg:"School of Business & Accountancy", courseDesr:"Aims to equip students with essential business knowledge and specialised training in accountancy and financial management to pursue a career in the Accountancy Sector.", courseType:"Part-Time"},
        { id: 2, qualific:"Degree in", courseName:"Sociology", institution:"National University of Singapore", schoolCtg:"Department of Sociology", courseDesr:"Aims to equip students with essential business knowledge and specialised training in arts and social politics.", courseType:"Full-Time"},
        { id: 3, qualific:"Degree in", courseName:"Sociology", institution:"National University of Singapore", schoolCtg:"Department of Sociology", courseDesr:"Aims to equip students with essential business knowledge and specialised training in arts and social politics.", courseType:"Full-Time"},
    ]
*/
    {/* Frontend */}
    
    return (
        <div id='dashboardContainer'>
            <div>
                <h1>COURSES</h1>
            </div>
            
            <div id='cards'>
                {courses.map((course) => (
                    <CourseCard 
                    key={course.id}
                    qualific={getQualific(course.level)}
                    courseName={course.course_name}
                    institution={course.institution}
                    schoolCtg={course.school}
                    courseDesr={course.course_description}
                    courseType="Full-Time"
                />
                ))}
            </div>

            <div className='cardBtns'>
                <Link to="/"><button>Back</button></Link> {/* To be changed: Direct to different pages for different user */}
                <Link to="/comparePage"><button>Compare</button></Link>
            </div>
        </div>
    )
}
