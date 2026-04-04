import { Link } from "react-router-dom";
import { getApiBaseUrl } from "../lib/api";

const phases = [
  "Map skills, interests, and goals through a guided assessment flow.",
  "Rank top-fit careers with transparent scoring and clear reasoning.",
  "Convert each recommendation into a practical roadmap with next steps."
];

export default function HomePage() {
  return (
    <div className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">Career discovery, rebuilt</p>
          <h1>Find the right career path and the fastest route to get there.</h1>
          <p className="hero-copy">
            Explore career paths with a platform that combines structured
            assessment, explainable recommendations, and roadmap planning in one
            clean experience.
          </p>
          <div className="hero-actions">
            <Link className="primary-link" to="/assessment">
              Start Assessment
            </Link>
            <span className="api-badge">API: {getApiBaseUrl()}</span>
          </div>
        </div>
        <aside className="hero-panel">
          <h2>What this platform gives you</h2>
          <ul>
            <li>Live assessment powered by a real backend and database</li>
            <li>Top-match career scoring with clear fit explanations</li>
            <li>Skill-gap analysis and guided next-step resources</li>
            <li>Admin tools for careers, skills, and roadmap content</li>
          </ul>
        </aside>
      </section>

      <section className="section" id="how-it-works">
        <p className="section-label">How it works</p>
        <div className="phase-grid">
          {phases.map((phase) => (
            <article className="phase-card" key={phase}>
              <p>{phase}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section" id="roadmap">
        <p className="section-label">Platform status</p>
        <div className="roadmap-card">
          <p>
            The platform is now live with auth, assessments, recommendations,
            private history, roadmap resources, analytics, and admin CRUD.
          </p>
        </div>
      </section>
    </div>
  );
}
