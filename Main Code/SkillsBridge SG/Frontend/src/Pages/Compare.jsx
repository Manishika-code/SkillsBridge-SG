import '../Pages/Compare.css';
import { useEffect, useState, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import BackBar from '../Components/BackBar';
import CourseCard from '../Components/Compare(component)'; // chart-enhanced component

const API_BASE = "http://localhost:8000/api";

export default function Compare() {
  const [searchParams] = useSearchParams();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const hasFetched = useRef(false);

  const courseIds = searchParams.get("courseIds")?.split(",").map(id => id.trim()) || [];
  const source = searchParams.get("source");

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

        // Fetch all base course info
        const courseResponses = await Promise.all(
          courseIds.map(id =>
            fetch(`${API_BASE}/courses/${id}/`).then(res => {
              if (!res.ok) throw new Error(`Course ${id} not found`);
              return res.json();
            })
          )
        );

        // Enrich with intake, IGP, GES, etc.
        const enriched = await Promise.all(
          courseResponses.map(async (course) => {
            const [
              igpRes,
              pathwaysRes,
              careersRes,
              intakeRes,
              gesRes
            ] = await Promise.all([
              fetch(`${API_BASE}/igp/?course__id=${course.id}`).then(r => r.ok ? r.json() : []),
              fetch(`${API_BASE}/pathways/?diploma__id=${course.id}`).then(r => r.ok ? r.json() : []),
              fetch(`${API_BASE}/career-paths/?course__id=${course.id}`).then(r => r.ok ? r.json() : []),
              fetch(`${API_BASE}/intake-by-institution/?institution=${encodeURIComponent(course.institution)}`).then(r => r.ok ? r.json() : []),
              fetch(`${API_BASE}/ges/?course__id=${course.id}`).then(r => r.ok ? r.json() : []),
            ]);

            // 🏫 Enrolment (institution-level, fallback-safe)
            let enrolment;
            if (intakeRes?.length) {
              const latest = intakeRes.at(-1);
              enrolment = {
                annualIntake: latest?.total_intake || 0,
                totalEnrolment: intakeRes.reduce((sum, e) => sum + (e.total_intake || 0), 0),
                internationalPct: latest?.intl_pct || 0,
                genderRatio: {
                  male: latest?.male_pct || 50,
                  female: latest?.female_pct || 50,
                },
                totalsByYear: intakeRes.map(e => ({
                  year: e.year,
                  total: e.total_intake,
                })),
              };
            } else {
              enrolment = {
                annualIntake: 300,
                totalEnrolment: 1200,
                internationalPct: 10,
                genderRatio: { male: 55, female: 45 },
                totalsByYear: [
                  { year: 2019, total: 950 },
                  { year: 2020, total: 1000 },
                  { year: 2021, total: 1100 },
                  { year: 2022, total: 1180 },
                  { year: 2023, total: 1210 },
                ],
              };
              console.warn(`⚠️ Using fallback enrolment for ${course.course_name}`);
            }

            // 🎓 Entry requirements (safe conversion)
            let requirements;
            if (igpRes?.length) {
              const rawGPA = igpRes.find(i => i.grade_type === "GPA")?.indicative_grade;
              const parsedGPA = parseFloat(rawGPA);
              requirements = {
                minGPA: !isNaN(parsedGPA) ? parsedGPA : "—",
                minALevel: igpRes.find(i => ["Rank Points", "alevel"].includes(i.grade_type))?.indicative_grade || "—",
                backgroundSplit: [
                  { source: "Polytechnic", pct: 60 },
                  { source: "Junior College", pct: 40 },
                ],
              };
            } else {
              requirements = {
                minGPA: 3.5,
                minALevel: "BBB/C",
                backgroundSplit: [
                  { source: "Polytechnic", pct: 55 },
                  { source: "Junior College", pct: 45 },
                ],
              };
              console.warn(`⚠️ Using fallback IGP for ${course.course_name}`);
            }

            // 💼 Employability (safe numbers)
            let employability;
            if (gesRes?.length) {
              const rate = parseFloat(gesRes[0]?.employment_rate) || 0;
              const salary = parseFloat(gesRes[0]?.median_salary) || 0;
              employability = {
                employmentRatePct: rate,
                medianSalary: salary,
                rateByYear: gesRes.map(g => ({
                  year: g.year,
                  rate: parseFloat(g.employment_rate) || 0,
                })),
                 roleShare: careersRes.map(c => ({
  name: c.career?.name || c.name,
})),             };
            } else {
              employability = {
                employmentRatePct: 90,
                medianSalary: 3400,
                rateByYear: [
                  { year: 2020, rate: 88 },
                  { year: 2021, rate: 89 },
                  { year: 2022, rate: 90 },
                  { year: 2023, rate: 91 },
                ],
                roleShare: [
                  { name: "Software Engineer", pct: 40 },
                  { name: "Data Analyst", pct: 35 },
                  { name: "Cybersecurity Analyst", pct: 25 },
                ],
              };
              console.warn(`⚠️ Using fallback GES data for ${course.course_name}`);
            }

            return {
              ...course,
              igp: igpRes,
              pathways: pathwaysRes.map(p => p.degree),
              careers: careersRes.map(c => c.career),
              enrolment,
              requirements,
              employability,
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
        <BackBar to={`/dashboardPage?skills=${searchParams.get("skills") || ""}&level=${searchParams.get("level") || ""}&source=${source}`} />
        <p style={{ textAlign: "center" }}>Loading comparison data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="compare-container">
        <BackBar to={`/dashboardPage?skills=${searchParams.get("skills") || ""}&level=${searchParams.get("level") || ""}&source=${source}`} />
        <p style={{ textAlign: "center", color: "red" }}>{error}</p>
      </div>
    );
  }

  if (courses.length === 0) {
    return (
      <div className="compare-container">
        <BackBar to={`/dashboardPage?skills=${searchParams.get("skills") || ""}&level=${searchParams.get("level") || ""}&source=${source}`} />
        <p style={{ textAlign: "center" }}>No comparison data available.</p>
      </div>
    );
  }

  return (
    <div className="compare-container">
      <BackBar to={`/dashboardPage?skills=${searchParams.get("skills") || ""}&level=${searchParams.get("level") || ""}&source=${source}`} />
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

