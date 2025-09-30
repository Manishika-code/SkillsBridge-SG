import '../Pages/Dashboard.css';
import { Link } from "react-router-dom";
import CourseCard from '../Components/CourseCard';
import { useEffect, useState } from 'react';

import { FiArrowLeftCircle } from "react-icons/fi";
import { FcInfo } from "react-icons/fc";
import { FaBookBookmark } from "react-icons/fa6";

// For institution display
const getQualific = (level) => {
    switch(level){
        case "poly": return "Diploma in";
        case "uni": return "Bachelor of";
        default: return '';
    }
}

// For only course name display
const cleanCourseName = (courseName) => {
    if (!courseName) return '';

    const prefixPoly = "Diploma in";
    const prefixUni = "Bachelor of";
    if (courseName.toLowerCase().startsWith(prefixPoly.toLowerCase())){
        return courseName.substring(prefixPoly.length).trim();
    }
    if (courseName.toLowerCase().startsWith(prefixUni.toLowerCase())){
        return courseName.substring(prefixUni.length).trim();
    }
    return courseName;
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


    {/* Frontend */}    
    return (
        <div id="wholeDashboard">               
            <div id='dashboardContainer'>                
                <div id="topPanel">
                    <div>
                        <Link to="/"><div className='backBtn'><FiArrowLeftCircle size={40} /></div></Link> {/* To be changed: Direct to different pages for different user */}                
                    </div>
                    <div>
                        <h1>COURSES</h1>
                    </div>
                </div>

                <div id='cards'>
                    {courses.map((course) => (
                        <CourseCard 
                        key={course.id}
                        qualific={getQualific(course.level)}
                        courseName={cleanCourseName(course.course_name)}
                        institution={course.institution}
                        schoolCtg={course.school}
                        courseDesr={course.course_description}
                        courseType="Full-Time"
                    />
                    ))}
                </div>

                <div className='compareBtn'>
                    <Link to="/comparePage"><div className='compareIco'><FcInfo size={60}/></div></Link>
                </div>
            </div>

            <div id="sideContainer">
                <div id="beforeSelect">                   
                    <div id='myBookmarks'>
                        <button><FaBookBookmark /> Check Out My Bookmarks</button>
                    </div>

                    <div className='infoDisplay'>
                        <h3>Select a course to find out more!</h3>
                        <h3>---</h3>
                        <h3>Click on <FcInfo size={40}/> to compare courses!</h3>
                    </div>
                </div>
            </div>
        </div>
    )
}
