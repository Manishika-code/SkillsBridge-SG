import '../Components/Compare(component).css';
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer,
  BarChart, Bar, CartesianGrid, PieChart, Pie, Cell, Legend
} from 'recharts';

const PIE_COLORS = ["#ef4444", "#22c55e", "#3b82f6"]; // red, green, blue

// Helper: build nice ticks at fixed "step" (e.g., 500)
function makeTicks(data, key, step = 500) {
  if (!data?.length) return { ticks: [0, step], domain: [0, step] };
  const max = Math.max(...data.map(d => Number(d[key]) || 0));
  const maxTick = Math.ceil(max / step) * step;
  const ticks = [];
  for (let t = 0; t <= maxTick; t += step) ticks.push(t);
  return { ticks, domain: [0, maxTick] };
}

// Safe formatters
const formatGPA = (val) => {
  const num = parseFloat(val);
  return !isNaN(num) ? num.toFixed(2) : "—";
};
const formatPct = (val) => {
  const num = parseFloat(val);
  return !isNaN(num) ? `${num.toFixed(1)}%` : "—";
};
const formatMoney = (val) => {
  const num = parseFloat(val);
  return !isNaN(num) ? `$${num.toLocaleString()}` : "—";
};

const HeaderH4 = ({ children }) => (
  <h4 style={{ fontSize: 20, fontWeight: 800, margin: '0 0 8px 0', textAlign: 'center' }}>
    {children}
  </h4>
);

const CourseCard = (course) => {
  const {
    qualific, courseName, institution, schoolCtg,
    courseDesr, courseType, enrolment, employability, requirements
  } = course;

  // 🧠 Aggregate duplicates so each year appears once
  const yearlyTotals = enrolment?.totalsByYear
    ? Object.values(
        enrolment.totalsByYear.reduce((acc, e) => {
          if (!acc[e.year]) acc[e.year] = { year: e.year, total: 0 };
          acc[e.year].total += e.total || 0;
          return acc;
        }, {})
      ).sort((a, b) => a.year - b.year)
    : [];

  const enrolTickCfg = makeTicks(yearlyTotals, 'total', 500);

  return (
    <div className="course-card">
      <div className="cardContent">
        {/* Header */}
        <h3 className="qualific">{qualific}</h3>
        <h1 className="courseName">{courseName}</h1>
        <hr />
        <p className="sub-desc">{institution} | {schoolCtg}</p>
        <p>{courseDesr}</p>

        {/* ===== Enrolment Statistics ===== */}
        {enrolment && (
          <section className="section">
            <HeaderH4>Institution Enrolment Statistics</HeaderH4>

            <div className="kpis">
              <div><strong>Annual Intake:</strong><br />~{enrolment.annualIntake} students</div>
              <div><strong>Total Enrolment:</strong><br />~{enrolment.totalEnrolment} across all years</div>
              <div><strong>Gender Ratio:</strong><br />{formatPct(enrolment.genderRatio.male)} Male, {formatPct(enrolment.genderRatio.female)} Female</div>
            </div>

            <div className="chart-wrap">
              <div className="chart-title">Total Students in Programme by Year:</div>
              <ResponsiveContainer width="100%" height={260}>
                <LineChart
                  data={yearlyTotals}
                  margin={{ left: 50, right: 50, top: 50, bottom: 50 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="year"
                    tick={{ fill: "#111", fontWeight: 800, fontSize: 13, dy: 6 }}
                    tickMargin={12}
                    label={{
                      value: "Year",
                      position: "bottom",
                      offset: 40,
                      style: { fill: "#111", fontWeight: 800, fontSize: 14 }
                    }}
                  />
                  <YAxis
                    ticks={enrolTickCfg.ticks}
                    domain={enrolTickCfg.domain}
                    allowDecimals={false}
                    tick={{ fill: "#111", fontWeight: 800, fontSize: 13, dx: -2 }}
                    tickMargin={10}
                    label={{
                      value: "Total Students",
                      angle: -90,
                      position: "left",
                      offset: 20,
                      style: { fill: "#111", fontWeight: 800, fontSize: 14 }
                    }}
                  />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="total"
                    stroke="#111"
                    strokeWidth={3}
                    dot={{ r: 3 }}
                    activeDot={{ r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </section>
        )}

        {/* ===== Requirements ===== */}
        {requirements && (
          <section className="section">
            <HeaderH4>Requirements</HeaderH4>

            <div className="kpis">
              <div><strong>Min GPA (Poly):</strong><br />{formatGPA(requirements.minGPA)} / 4.00</div>
              <div><strong>Min A-Level Score:</strong><br />{requirements.minALevel || "—"}</div>
            </div>
                      </section>
        )}

        {/* ===== Employability ===== */}
        {employability && (
          <section className="section">
            <HeaderH4>Graduate Employment Rate</HeaderH4>

            <div className="kpis">
              <div><strong>Employment Rate:</strong><br />{formatPct(employability.employmentRatePct)}</div>
              <div><strong>Median Salary:</strong><br />{formatMoney(employability.medianSalary)}</div>
            </div>

            <div className="chart-wrap">
              <div className="chart-title">Employment Rate by Year:</div>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart
                  data={employability.rateByYear}
                  margin={{ left: 50, right: 50, top: 50, bottom: 50 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="year"
                    tick={{ fill: "#111", fontWeight: 800, fontSize: 13, dy: 6 }}
                    tickMargin={12}
                    label={{
                      value: "Year",
                      position: "bottom",
                      offset: 40,
                      style: { fill: "#111", fontWeight: 800, fontSize: 14 }
                    }}
                  />
                  <YAxis
                    domain={[0, 100]}
                    tick={{ fill: "#111", fontWeight: 800, fontSize: 13, dx: -2 }}
                    tickMargin={10}
                    label={{
                      value: "Employment Rate (%)",
                      angle: -90,
                      position: "left",
                      offset: 20,
                      style: { fill: "#111", fontWeight: 800, fontSize: 10 }
                    }}
                  />
                  <Tooltip formatter={(v) => `${v}%`} />
                  <Bar dataKey="rate" fill="#111827" />
                </BarChart>
              </ResponsiveContainer>
            </div>
{/* LIST: Popular Job Roles */}
{employability.roleShare?.length > 0 && (
  <div className="chart-wrap">
    <div className="chart-title">Popular Job Roles:</div>
    <div className="career-list">
      {employability.roleShare.map((role, idx) => (
        <div key={idx} className="career-item">
          <strong>{role.name}</strong>
        </div>
      ))}
    </div>
  </div>
)}
                      </section>
        )}
      </div>
    </div>
  );
};

export default CourseCard;

