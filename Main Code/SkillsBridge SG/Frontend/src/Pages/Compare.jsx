import '../Pages/Compare.css';
import { useEffect, useState, useRef } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import BackBar from '../Components/BackBar';
import CourseCard from '../Components/Compare(component)'; // chart-enhanced component

const API_BASE = "http://localhost:8000/api";

export default function Compare() {
  const [searchParams] = useSearchParams();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const courseIds = searchParams.get("courseIds")?.split(",").map(id => id.trim()) || [];
  const hasFetched = useRef(false);
  const source = searchParams.get('source');

  console.log(source);

  useEffect(() => {
    if (hasFetched.current) return;
    hasFetched.current = true;

    if (courseIds.length === 0) {
      setError("No courses selected for comparison.");
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        setLoading(true);

        // Fetch all base course data
        const courseResponses = await Promise.all(
          courseIds.map(id =>
            fetch(`${API_BASE}/courses/${id}/`).then(res => {
              if (!res.ok) throw new Error(`Course ${id} not found`);
              return res.json();
            })
          )
        );

        // Attach IGP, Pathways, and Careers data
        const enriched = await Promise.all(
          courseResponses.map(async (course) => {
            const [igpRes, pathwaysRes, careersRes] = await Promise.all([
              fetch(`${API_BASE}/igp/?course__id=${course.id}`).then(r => r.ok ? r.json() : []),
              fetch(`${API_BASE}/pathways/?diploma__id=${course.id}`).then(r => r.ok ? r.json() : []),
              fetch(`${API_BASE}/career-paths/?course__id=${course.id}`).then(r => r.ok ? r.json() : []),
            ]);

            // 🧠 Derive richer visual data for charts (mock/fallbacks)
            const enrichEnrolment = {
              annualIntake: 300,
              totalEnrolment: 1200,
              internationalPct: 12,
              genderRatio: { male: 55, female: 45 },
              totalsByYear: [
                { year: 2021, total: 1100 },
                { year: 2022, total: 1150 },
                { year: 2023, total: 1180 },
                { year: 2024, total: 1200 },
              ],
            };

            const enrichRequirements = {
              minGPA: 3.5,
              minALevel: igpRes?.[0]?.indicative_grade || "AAA/B",
              backgroundSplit: [
                { source: "Polytechnic", pct: 60 },
                { source: "Junior College", pct: 40 },
              ],
            };

            const enrichEmployability = {
              employmentRatePct: parseInt(course.employment_rate || "90"),
              medianSalary: parseInt(course.median_salary || "3400"),
              rateByYear: [
                { year: 2021, rate: 88 },
                { year: 2022, rate: 89 },
                { year: 2023, rate: 90 },
                { year: 2024, rate: 91 },
              ],
              roleShare: [
                { name: "Software Engineer", pct: 40 },
                { name: "Data Analyst", pct: 35 },
                { name: "Cybersecurity Analyst", pct: 25 },
              ],
            };

            return {
              ...course,
              igp: igpRes,
              pathways: pathwaysRes.map(p => p.degree),
              careers: careersRes.map(c => c.career),
              enrolment: enrichEnrolment,
              requirements: enrichRequirements,
              employability: enrichEmployability,
            };
          })
        );

        setCourses(enriched);
      } catch (err) {
        console.error("Error loading compare data:", err);
        setError("Failed to load comparison data.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [courseIds]);

  const getQualific = (level) => {
    switch (level) {
      case "poly": return "Diploma in";
      case "uni": return "Bachelor of";
      default: return "";
    }
  };

  const cleanCourseName = (name) =>
    name ? name.replace(/^Diploma in\s*/i, "").replace(/^Bachelor of\s*/i, "").trim() : "";

  if (loading) {
    return (
      <div className="compare-container">
        <BackBar to={`/dashboardPage?source=${source}`}/>
        <p style={{ textAlign: "center" }}>Loading comparison data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="compare-container">
        <BackBar to={`/dashboardPage?source=${source}`}/>
        <p style={{ textAlign: "center", color: "red" }}>{error}</p>
      </div>
    );
  }

  if (courses.length === 0) {
    return (
      <div className="compare-container">
        <BackBar to={`/dashboardPage?source=${source}`}/>
        <p style={{ textAlign: "center" }}>No comparison data available.</p>
      </div>
    );
  }

  return (
    <div className="compare-container">
      <BackBar to={`/dashboardPage?source=${source}`}/>

      <div className="cardRow">
        {courses.map((course) => (
          <CourseCard
            key={course.id}
            qualific={getQualific(course.level)}
            courseName={cleanCourseName(course.course_name)}
            institution={course.institution}
            schoolCtg={course.school}
            courseDesr={course.course_description}
            courseType="Full-Time"
            enrolment={course.enrolment}
            requirements={course.requirements}
            employability={course.employability}
          />
        ))}
      </div>
    </div>
  );
}

