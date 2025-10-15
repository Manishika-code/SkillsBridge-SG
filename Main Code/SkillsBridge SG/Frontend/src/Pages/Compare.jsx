import '../Pages/Compare.css';
import CourseCard from '../Components/Compare(component)';
import { Link } from "react-router-dom";

export default function Compare(){
  const course1 = {
    qualific:"Diploma in",
    courseName:"Accountancy",
    institution:"Ngee Ann Polytechnic",
    schoolCtg:"School of Business & Accountancy",
    courseDesr:
      "Aims to equip students with essential business knowledge and specialised training in accountancy and financial management to pursue a career in the Accountancy Sector.",
    courseType:"Part-Time",

    enrolment: {
      annualIntake: 320,
      totalEnrolment: 1250,
      internationalPct: 18,
      genderRatio: { male: 60, female: 40 }, // kept for text KPI only
      totalsByYear: [
        { year: 2021, total: 1180 },
        { year: 2022, total: 1205 },
        { year: 2023, total: 1230 },
        { year: 2024, total: 1250 }
      ]
    },

    requirements: {
      minGPA: 3.5,               // out of 4.0 (example)
      minALevel: "BBB/B",        // example string
      backgroundSplit: [
        { source: "Polytechnic", pct: 65 },
        { source: "Junior College", pct: 35 }
      ]
    },

    employability: {
      employmentRatePct: 91,
      medianSalary: 3300,
      rateByYear: [
        { year: 2021, rate: 89 },
        { year: 2022, rate: 90 },
        { year: 2023, rate: 91 },
        { year: 2024, rate: 91 }
      ],
      roleShare: [
        { name: "Tax Associate", pct: 40 },
        { name: "Audit Assistant", pct: 35 },
        { name: "Payroll Officer", pct: 25 }
      ]
    }
  };

  const course2 = {
    qualific:"Degree in",
    courseName:"Sociology",
    institution:"National University of Singapore",
    schoolCtg:"Department of Sociology",
    courseDesr:
      "Aims to equip students with essential business knowledge and specialised training in arts and social politics.",
    courseType:"Full-Time",

    enrolment: {
      annualIntake: 480,
      totalEnrolment: 1650,
      internationalPct: 22,
      genderRatio: { male: 45, female: 55 },
      totalsByYear: [
        { year: 2021, total: 1550 },
        { year: 2022, total: 1600 },
        { year: 2023, total: 1630 },
        { year: 2024, total: 1650 }
      ]
    },

    requirements: {
      minGPA: 3.8,
      minALevel: "ABB/B",
      backgroundSplit: [
        { source: "Polytechnic", pct: 30 },
        { source: "Junior College", pct: 70 }
      ]
    },

    employability: {
      employmentRatePct: 88,
      medianSalary: 3600,
      rateByYear: [
        { year: 2021, rate: 86 },
        { year: 2022, rate: 87 },
        { year: 2023, rate: 88 },
        { year: 2024, rate: 88 }
      ],
      roleShare: [
        { name: "Social Researcher", pct: 45 },
        { name: "Policy Analyst", pct: 30 },
        { name: "Human Resources Specialist", pct: 25 }
      ]
    }
  };

  return (
    <div className='compare-container'>
      <h1>Compare Results</h1>
      <div className="cardRow">
        <CourseCard {...course1} />
        <CourseCard {...course2} />
      </div>
      <div className="backButton">
        <Link to="/dashboardPage"><button>Back</button></Link>
      </div>
    </div>
  );
}
