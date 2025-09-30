import '../Pages/Dashboard.css';
import { Link } from "react-router-dom";
import CourseCard from '../Components/CourseCard';
import { useEffect, useState } from 'react';

export default function Dashboard(){  
    {/* Define functionality / datasets */}



    const populateCourseCards = [
        { id: 1, qualific:"Diploma in", courseName:"Accountancy", institution:"Ngee Ann Polytechnic", schoolCtg:"School of Business & Accountancy", courseDesr:"Aims to equip students with essential business knowledge and specialised training in accountancy and financial management to pursue a career in the Accountancy Sector.", courseType:"Part-Time"},
        { id: 2, qualific:"Degree in", courseName:"Sociology", institution:"National University of Singapore", schoolCtg:"Department of Sociology", courseDesr:"Aims to equip students with essential business knowledge and specialised training in arts and social politics.", courseType:"Full-Time"},
        { id: 3, qualific:"Degree in", courseName:"Sociology", institution:"National University of Singapore", schoolCtg:"Department of Sociology", courseDesr:"Aims to equip students with essential business knowledge and specialised training in arts and social politics.", courseType:"Full-Time"},
    ]

    {/* Frontend */}
    
    return (
        <div id='dashboardContainer'>
            <div>
                <h1>COURSES</h1>
            </div>
            
            <div id='cards'>
                {populateCourseCards.map((course) => (
                    <CourseCard 
                    key={course.id}
                    qualific={course.qualific}
                    courseName={course.courseName}
                    institution={course.institution}
                    schoolCtg={course.schoolCtg}
                    courseDesr={course.courseDesr}
                    courseType={course.courseType}
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