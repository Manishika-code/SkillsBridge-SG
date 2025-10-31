import '../Components/Compare(component).css';
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer,
  BarChart, Bar, CartesianGrid, PieChart, Pie, Cell, Legend
} from 'recharts';

const PIE_COLORS = ["#ef4444", "#22c55e", "#3b82f6"]; // red, green, blue

// Helper: build nice ticks at fixed "step" (e.g., 500) for a given data key
function makeTicks(data, key, step = 500) {
  if (!data?.length) return { ticks: [0, step], domain: [0, step] };
  const max = Math.max(...data.map(d => Number(d[key]) || 0));
  const maxTick = Math.ceil(max / step) * step;
  const ticks = [];
  for (let t = 0; t <= maxTick; t += step) ticks.push(t);
  return { ticks, domain: [0, maxTick] };
}

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

  // Build 500-step ticks for the enrolment totals line
  const enrolTickCfg = enrolment?.totalsByYear
    ? makeTicks(enrolment.totalsByYear, 'total', 500)
    : { ticks: [0, 500, 1000, 1500], domain: [0, 1500] };

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
            <HeaderH4>Enrolment Statistics</HeaderH4>

            <div className="kpis">
              <div><strong>Annual Intake:</strong><br />~{enrolment.annualIntake} students</div>
              <div><strong>Total Enrolment:</strong><br />~{enrolment.totalEnrolment} across all years</div>
              <div><strong>Gender Ratio:</strong><br />{enrolment.genderRatio.male}% Male, {enrolment.genderRatio.female}% Female</div>
              <div><strong>International Students:</strong><br />{enrolment.internationalPct}%</div>
            </div>

            {/* LINE: Total students per year — labels OUTSIDE + 500-step ticks */}
            <div className="chart-wrap">
              <div className="chart-title">Total Students in Programme by Year:</div>
              <ResponsiveContainer width="100%" height={260}>
                <LineChart
                  data={enrolment.totalsByYear}
                  margin={{ left: 50, right: 50, top: 50, bottom: 50 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="year"
                    tick={{ fill: "#111", fontWeight: 800, fontSize: 13, dy: 6 }}
                    tickMargin={12}
                    label={{
                      value: "Year",
                      position: "bottom",               // OUTSIDE bottom
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
                      position: "left",                // OUTSIDE left
                      offset: 20,
                      style: { fill: "#111", fontWeight: 800, fontSize: 14 }
                    }}
                  />
                  <Tooltip />
                  <Line type="monotone" dataKey="total" stroke="#111" strokeWidth={3} dot />
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
              <div><strong>Min GPA (Poly):</strong><br />{requirements.minGPA.toFixed(2)} / 4.00</div>
              <div><strong>Min A-Level Score:</strong><br />{requirements.minALevel}</div>
            </div>

            {/* BAR: Poly vs JC — labels OUTSIDE */}
            <div className="chart-wrap">
              <div className="chart-title">Intake Background Split:</div>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart
                  data={requirements.backgroundSplit}
                  margin={{ left: 50, right: 50, top: 50, bottom: 50 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="source"
                    tick={{ fill: "#111", fontWeight: 800, fontSize: 13, dy: 6 }}
                    tickMargin={12}
                    label={{
                      value: "Background",
                      position: "bottom",             // OUTSIDE
                      offset: 40,
                      style: { fill: "#111", fontWeight: 800, fontSize: 14 }
                    }}
                  />
                  <YAxis
                    domain={[0, 100]}
                    tick={{ fill: "#111", fontWeight: 800, fontSize: 13, dx: -2 }}
                    tickMargin={10}
                    label={{
                      value: "Percent of Cohort",
                      angle: -90,
                      position: "left",              // OUTSIDE
                      offset: 20,
                      style: { fill: "#111", fontWeight: 800, fontSize: 14 }
                    }}
                  />
                  <Tooltip formatter={(v) => `${v}%`} />
                  <Bar dataKey="pct" fill="#4B5563" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </section>
        )}

        {/* ===== Employability ===== */}
        {employability && (
          <section className="section">
            <HeaderH4>Graduate Employment Rate</HeaderH4>

            <div className="kpis">
              <div><strong>Employment Rate:</strong><br />{employability.employmentRatePct}%</div>
              <div><strong>Median Salary:</strong><br />${employability.medianSalary.toLocaleString()}</div>
            </div>

            {/* BAR: Employment rate by year — labels OUTSIDE */}
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
                      position: "bottom",           // OUTSIDE
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
                      position: "left",            // OUTSIDE
                      offset: 20,
                      style: { fill: "#111", fontWeight: 800, fontSize: 10 }
                    }}
                  />
                  <Tooltip formatter={(v) => `${v}%`} />
                  <Bar dataKey="rate" fill="#111827" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* PIE: Role share — compact */}
            {employability.roleShare && (
              <div className="chart-wrap">
                <div className="chart-title">Share by Popular Job Roles:</div>
                <ResponsiveContainer width="100%" height={260}>
                  <PieChart margin={{ top: 8, bottom: 8 }}>
                    <Tooltip formatter={(v) => `${v}%`} />
                    <Legend
                      verticalAlign="bottom"
                      align="center"
                      wrapperStyle={{ color: "#111", fontWeight: 800 }}
                    />
                    <Pie
                      data={employability.roleShare}
                      dataKey="pct"
                      nameKey="name"
                      cx="50%"
                      cy="42%"
                      outerRadius={80}
                      labelLine={false}
                    >
                      {employability.roleShare.map((_, i) => (
                        <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                      ))}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
              </div>
            )}
          </section>
        )}
      </div>
    </div>
  );
};

export default CourseCard;





