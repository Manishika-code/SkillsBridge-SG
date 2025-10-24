import './Home.css';
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div id="homeContainer">
      {/* top bar */}
      <header id="topBar">
        <span id="logoText">SkillsBridgeSG</span>
      </header>

      {/* hero section */}
      <section id="heroSection">
        <h2>PERSONALISED EDUCATIONAL ROADMAPS</h2>
        <h1>Your Future Starts Here !</h1>

        <div id="buttonRow">
          <Link to="/dashboardPage?source=visitor"><button>Visitor</button></Link>
          <Link to="/loginPage?source=login"><button>Login</button></Link>
        </div>
      </section>

      {/* how it works */}
      <section id="howItWorks">
        <h3>HOW IT WORKS?</h3>

        <div id="stepsRow">
          <div className="step">
            <div className="circle">1</div>
            <p>Select your interests/skills<br />and qualifications</p>
          </div>

          {/* four small bubbles between 1 and 2 */}
          <div className="miniDots">
            <span></span><span></span><span></span><span></span>
          </div>

          <div className="step">
            <div className="circle">2</div>
            <p>View all suitable courses<br />with roadmaps and data</p>
          </div>

          {/* four small bubbles between 2 and 3 */}
          <div className="miniDots">
            <span></span><span></span><span></span><span></span>
          </div>

          <div className="step">
            <div className="circle">3</div>
            <p>Compare courses to pick<br />the most suitable one</p>
          </div>
        </div>
      </section>
    </div>
  );
}
