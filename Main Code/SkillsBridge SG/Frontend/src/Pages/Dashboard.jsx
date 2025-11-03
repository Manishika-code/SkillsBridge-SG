import { Link, useSearchParams } from "react-router-dom";
import { useEffect, useState } from 'react';
import '../Pages/Dashboard.css';

// Referencing Components
import CourseCard from '../Components/CourseCard';
import GridCourseInfo from '../Components/CourseInfoGrid';
import CourseRoadMapList from '../Components/CourseRoadMapList';
import Dropdown from "../Components/Dropdown";

// Icons Used
import { FiArrowLeftCircle } from "react-icons/fi";
import { FcInfo } from "react-icons/fc";
import { FaBookBookmark } from "react-icons/fa6";
import { FaBookmark } from "react-icons/fa"; // for bookmark-ed
import { MdCancel } from "react-icons/md";
import { FaRegBookmark } from "react-icons/fa6";

// Backend base URL 
const API_BASE = "http://localhost:8000/api";

// Get login access token 
const getToken = () => {
  if (typeof window !== "undefined") {
    return localStorage.getItem("access");
  }
  return null;
};

{/* Display of data logic */}
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

// Bookmark API functions
const getBookMarkedCourses = async () => {
  try {
    const res = await fetch(`${API_BASE}/bookmarks/`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    });
    if (!res.ok) throw new Error("Failed to fetch bookmarks");
    const data = await res.json();
    return data.map(b => b.course);
  } catch (err) {
    console.error(err);
    return [];
  }
};

const addBookmark = async (courseId) => {
  try {
    const res = await fetch(`${API_BASE}/bookmarks/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`,
      },
      body: JSON.stringify({course_id: courseId}),
    });
    if (res.status === 201) {
      alert("Added to bookmarks");
      return true;
    } else if (res.status === 200) {
      alert("Already bookmarked");
      return false;
    } else {
      throw new Error("Error adding bookmark");
    }
  } catch (err) {
    console.error(err);
    alert("Failed to add bookmark");
    return false;
  }
};

const removeBookmark = async (courseId) => {
  try {
    const res = await fetch(`${API_BASE}/bookmarks/${courseId}/`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    });
    if (res.status == 204) {
        alert("Bookmark removed");
        return true;
    } else if (res.status === 200) {
        alert("Already bookmarked");
      return false;
    } else {
        throw new Error("Error adding bookmark");
    } 
  } catch (err) {
      console.error(err);
      alert("Failed to add bookmark");
      return false;
  }
};

// fetch course logic
// 
// {/* Bookmarked Management */}
// const getBookMarkedCourses = () => {
// 
//     console.log(localStorage.getItem('BookmarkedCourses')); // print out current list
// 
//     return JSON.parse(localStorage.getItem('BookmarkedCourses') || '[]');
// };
// 
// // Check if course bookedmarked
// const isCourseBookedMarked = (courseId) => {
//     const bm = getBookMarkedCourses();
//     return bm.includes(courseId);
// }
// 
// // Add bookmark to Local Storage
// const addBookmark = (courseId) => {
//     const bm = getBookMarkedCourses();
// 
//     if(!bm.includes(courseId)){
//         bm.push(courseId);
//         localStorage.setItem('BookmarkedCourses', JSON.stringify(bm));
// 
//         return true;
//     }
//     return false;
// }
// 
// // Remove bookmark from LS
// const removeBookmark = (courseId) => {
//     const bm = getBookMarkedCourses();
//     
//     const update = bm.filter(id => id !== courseId);
//     localStorage.setItem('BookmarkedCourses', JSON.stringify(update)); // adding all & replace current list, to exclude the one to remove
//     return true;
// }
// 
// 

{/* Main Dashboard Code */}
export default function Dashboard(){ 
     
    {/* ======== Defined datasets ======== */}
    const [courses, setCourses] = useState([]);
    const [viewMode, setViewMode] = useState(null);
    const [selectedId, setSelectedId] = useState(0); // A variable to fetch latest selected ID
    const [activeContent, setActiveContent] = useState("original");
    const [searchParams] = useSearchParams();

   const [igpInfo, setIgpInfo] = useState([]);
   const [degreePathways, setDegreePathways] = useState([]);
   const [careerPaths, setCareerPaths] = useState([]);

    // Default fetch all
    const skillsParam = searchParams.get("skills");
    const levelParam = searchParams.get("level");

    {/* ======== Navigation Interactions ======== */} 
    // Visitor or Logged In user 
    const source = searchParams.get('source');
    // check if coming from visitor
    const forVisitor = source === 'visitor';

    useEffect(() => {
      const savedSkills = JSON.parse(localStorage.getItem("selectedSkills") || "[]");
      const savedLevel = localStorage.getItem("selectedLevel");
      
      const finalSkills = skillsParam ? skillsParam.split(",") : savedSkills;
      const finalLevel = levelParam || savedLevel;
      
      if (finalSkills.length > 0) {
        fetchCoursesBySkills(finalSkills, finalLevel);
      } else {
        fetchAllCourses();
      }
    }, []);


    // Fetch ALL
    const fetchAllCourses = () => {
        fetch("http://localhost:8000/api/courses/")
        .then((res) => res.json())
        .then((data) => {
            setCourses(data);
            setViewMode(null);
    })
        .catch((err) => console.error("Error fetching courses:", err));
    }

    const fetchCoursesBySkills = (skillList, level) => {
            fetch(`${API_BASE}/courses/by-skills/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    skills: skillList,
                    level: level,
                }),
            })
                .then(res => res.json())
                .then(data => {
                    setCourses(data);
                    setViewMode(null);
                })
                .catch(err => console.error("Error fetching by skills:", err));
        };
    
    useEffect(() => {
      if (!selectedId) return;
    
      // Fetch IGP
      fetch(`${API_BASE}/igp/?course__id=${selectedId}`)
        .then(res => res.json())
        .then(data => setIgpInfo(data))
        .catch(err => console.error("Error fetching IGP:", err));
    
      // Fetch Pathways (Diploma → Degree)
      fetch(`${API_BASE}/pathways/?diploma__id=${selectedId}`)
        .then(res => res.json())
        .then(data => setDegreePathways(data.map(p => p.degree)))
        .catch(err => console.error("Error fetching Pathways:", err));
    
      // Fetch Careers (Course → Career)
      fetch(`${API_BASE}/career-paths/?course__id=${selectedId}`)
        .then(res => res.json())
        .then(data => setCareerPaths(data.map(p => p.career)))
        .catch(err => console.error("Error fetching Careers:", err));
    }, [selectedId]);

    const fetchBookmarks = async () => {
    const data = await getBookMarkedCourses();
    console.log("Bookmarked data:", data);
    setCourses(data);
    setViewMode("bookmarks");
  }
   
    
    {/* ======== BOOKMARK MANAGEMENT SYSTEM ======== */}
     // Bookmarked Management
    const toggleBookmarked = (isBookmark) => {
          if (isBookmark)
          {
              // show bookmarked only
              setViewMode("bookmarks");
          }
          else
          {
              // Show original
              setViewMode(null);
              window.location.reload();
          }
      }
    const handleBookMarkClick = async () => {
      const success = await addBookmark(selectedId);
      if (success) fetchBookmarks();
    };

    const removeBookMark = async () => {
      const success = await removeBookmark(selectedId);
      if (success) fetchBookmarks();
    };

    
    // Grid Info
    const gridInfo = [
        {id: 1, header: "Elr2b2 type", data: "A"},
        {id: 2, header: "Elr2b2", data: "4 to 11"},
        {id: 3, header: "Planned Intake", data: "150"},
    ]

    // RoadMap List (Degree)
    const degreeCourses = [
        {id: 1, itemName:"Accountancy"},
        {id: 2, itemName:"Business and Computing"},
        {id: 3, itemName:"Business (3-yr direct Honours Programme)"},
    ]

    // RoadMap List (Careers)
    const careers = [
        {id: 1, itemName:"Business Analyst"},
        {id: 2, itemName:"Accountant"},
        {id: 3, itemName:"Sales Analytics"},
    ]


    // Direct user to website function
    const directToWebsite = (courseId) =>{
      console.log("Direct to: ", courseId, "Website link");
    }

        
    // Selection Card display + Fetch selected ID
    const [selectedCard, setSelectedCard] = useState(null);
    const handleSelectedCard = (courseId) =>{
        setSelectedCard(courseId);
        setSelectedId(courseId); // Save selected ID
    }

    // Determine if any card selected first
    const hasSelection = selectedCard !== null;
    // Clear Selection
    const clearSelectionCard = () =>{
        setSelectedCard(null);
    }

    // Disable/Enable Compare button 
    const [isDisabled, setIsDisabled] = useState(true);

    // Toggle Checkbox for compare
    const [showToggleUI, setShowToggleUI] = useState(false);

    // Track which courses is selected
    const [selectedCourses, setSelectedCourses] = useState([]);

    // Handle checkbox state
    const handleCheckBox = (courseId, isChecked) => {
        if (isChecked){
            // Only allow 2 selections
            if (selectedCourses.length < 2)
            {
                const listSelectionCourses = [...selectedCourses, courseId];
                setSelectedCourses(listSelectionCourses);

                if (selectedCourses.length == 1)
                {
                    console.log(listSelectionCourses);  // Return a list with selected 2 courseID for compare
                    // Max comparisons reached, Enable Compare btn
                    setIsDisabled(false);
                }
            }
        }
        else
        {
            // Less than 2 selections now, Disable Compare btn
            setIsDisabled(true);
            // Remove item
            setSelectedCourses(selectedCourses.filter(id => id !== courseId));
        }
    }

    // Clear checkbox selection 
    const resetCheckbox = () =>{
        setSelectedCourses([]);
        setIsDisabled(true);
    }

    // Toggle function
    
    const toggleContentClick = (contentClicked) => {
        switch (contentClicked){
            case "card":
                // card clicked, show info
                setActiveContent("MoreInfo");
                break;  

            case "ExitToOriginal":
                // exit info, show original
                setActiveContent("original");
                setShowToggleUI(false);
                resetCheckbox();
                clearSelectionCard();
                break;
            
            case "compare":
                setActiveContent("compareUI");
                setShowToggleUI(!showToggleUI);
                break;

            default:
                setActiveContent("original");
                break;
        }
    };
    

    {/* Frontend */}    
    return (
        <div id="wholeDashboard">               
            <div id='dashboardContainer'>                
                <div id="topPanel">
                    <div>
                        {viewMode === null && (
                            <Link to={!forVisitor ? `/categoryPage?source=${source}` : "/"}><div className='backBtn'><FiArrowLeftCircle size={40} /></div></Link>               
                        )}

                        {viewMode === "bookmarks" && (
                            <Link to="/dashboardPage"><div className='backBtn' onClick = {() => {fetchAllCourses(); toggleBookmarked(false)}}><FiArrowLeftCircle size={40} /></div></Link>    
                        )}
                    </div>

                    <div>
                        {viewMode === null && (
                            <h1>COURSES</h1>
                        )}

                        {viewMode === "bookmarks" && (
                            <h1>MY BOOKMARKS</h1>
                        )}
                    </div>

                    <div className="filterBar">
                        <div className="filtersSection">
                          {/* Dropdown for polytechnics */}
                          <Dropdown 
                            options={[
                              {value: 'all', label:'-- All --'},
                              {value: 'np', label:'Ngee Ann Poly'},
                              {value: 'nyp', label:'Nanyang Poly'},
                              {value: 'sp', label:'Singapore Poly'},
                              {value: 'tp', label:'Temasek Poly'},
                              {value: 'rp', label:'Republic Poly'}
                            ]}
                            placeholder='Polytechnics'
                            onDropdownSelect={(option) => console.log("Selected", option)}
                          />

                          {/* Dropdown for universities*/}
                          <Dropdown 
                            options={[
                              {value: 'all', label:'-- All --'},
                              {value: 'nus', label:'NUS'},
                              {value: 'ntu', label:'NTU'},
                              {value: 'smu', label:'SMU'},
                              {value: 'sit', label:'SIT'},
                              {value: 'sutd/suss', label:'SUTD / SUSS'}
                            ]}
                            placeholder='Universities'
                            onDropdownSelect={(option) => console.log("Selected", option)}
                          />
                          
                        </div>

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

                        onCardClick={() => {toggleContentClick("card"); handleSelectedCard(course.id)}}
                        
                        isChecked={selectedCourses.includes(course.id)}
                        onCheckboxChange={(checked) => handleCheckBox(course.id, checked)}
                        
                        isSelected={selectedCard === course.id}
                        hasSelection={hasSelection}
                        showToggleUI={showToggleUI}
                        />
                    ))}
                </div>

                {activeContent === "original" && (
                    <div className='compareBtn'>
                        <button onClick={() => toggleContentClick("compare")}><div className='compareIco'><FcInfo size={60}/></div></button>                        
                    </div>
                )}
            </div>

            <div id="sideContainer">              
                {activeContent === "original" && (
                    <div id="beforeSelect">  
                        {/* Only show if NOT visitor */}
                        {!forVisitor && viewMode == null && (
                            <div id='myBookmarks'>
                                <button onClick={() => {fetchBookmarks(); toggleBookmarked(true)}}><FaBookBookmark /> Check Out My Bookmarks</button>
                            </div>
                        )}                 

                        <div className='infoDisplay'>
                            <h3>Select a course to find out more!</h3>
                            <h3>---</h3>
                            <h3>Click on <FcInfo size={40}/> to compare courses!</h3>
                        </div>
                    </div>
                )}
                
                {activeContent === "MoreInfo" && (
                  <div id="afterSelect">
                    <div id="latestInfo">
                        <div id="topBar">
                            <button className='cancelBtn' onClick={() => toggleContentClick("ExitToOriginal")}><MdCancel size={40}/></button>
                            
                            {/* Show only for login user */}
                            {!forVisitor && viewMode == null && (
                                <button className='bookmarkBtn' onClick={() => handleBookMarkClick()}><FaRegBookmark size={35}/></button>
                            )}

                            {/* Show when in bookedmark page */}
                            {viewMode === "bookmarks" && (
                                <button className='bookmarkBtn' onClick={() => removeBookMark()}><FaBookmark size={35}/></button>
                            )}

                        </div>
                    
                        <h1 className="headerSide">Latest Info</h1>                            
                        <div id="gridContent">
                          {igpInfo.length > 0 ? (
                            igpInfo.map((igp) => (
                              <GridCourseInfo
                                key={igp.id}
                                header={`${igp.qualification.toUpperCase()} (${igp.grade_type})`}
                                data={igp.indicative_grade}
                              />
                            ))
                          ) : (
                            <p>-- No IGP data available --</p>
                          )}
                        </div>
                    </div>

                    <div id="roadMap">
                        <h1 className="headerSide">Road Map</h1>  
                        <p>Recommended path outline in the future</p>

                        <div id="mapContainer">
                            {/* Applicable for Poly only */}
                            <div className="coursesContainer">
                                <div className="outerBorder">
                                    <h3>Degree Courses</h3>
                                    <div className="theList">
                                      {degreePathways.length > 0 ? (
                                        degreePathways.map((d) => (
                                          <CourseRoadMapList
                                            key={d.id}
                                            itemName={cleanCourseName(d.course_name)}
                                          />
                                        ))
                                      ) : (
                                        <p>No linked degree pathways found.</p>
                                      )}
                                    </div>
                                </div>
                            </div>

                            {/* Applicable for All */}
                            <div className="coursesContainer">
                                <div className="outerBorder">
                                    <h3>Careers</h3>

                                        <div className="theList">
                                          {careerPaths.length > 0 ? (
                                            careerPaths.map((career) => (
                                              <CourseRoadMapList key={career.id} itemName={career.name} />
                                            ))
                                          ) : (
                                            <p>No career data available.</p>
                                          )}
                                    </div>
                                </div>
                            </div>                            
                        </div> 
                    </div>

                    <div id="moreSection">
                        <button onClick={() => directToWebsite(selectedId)}>Learn More</button>
                    </div>
                  </div>                   
                )}

                {activeContent === "compareUI" &&(
                    <div id="compare"> 
                        <button className='cancelBtn' onClick={() => toggleContentClick("ExitToOriginal")}><MdCancel size={40}/></button>
                        <div id="compareGuide">

                            <div className='infoDisplay'>
                                <h2>Compare Courses</h2>
                                <h3>Select 2 courses to compare side-by-side!</h3>
                            </div>   

                            <div id="compareBtn">
                              <Link to={`/comparePage?courseIds=${selectedCourses.join(",")}&source=${source}`}>
                                <button disabled={isDisabled}>COMPARE!</button>
                              </Link>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
