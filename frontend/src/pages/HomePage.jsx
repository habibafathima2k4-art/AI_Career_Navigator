import { useEffect } from "react";
import { Link, useLocation } from "react-router-dom";

const phases = [
  {
    step: "01",
    title: "Assess your profile",
    subtitle: "Start with a guided snapshot",
    copy: "Map your skills, interests, work style, and salary goals through a guided assessment flow."
  },
  {
    step: "02",
    title: "See ranked matches",
    subtitle: "Understand why each fit appears",
    copy: "Rank top-fit careers with transparent scoring, matched strengths, and clear recommendation reasoning."
  },
  {
    step: "03",
    title: "Follow the roadmap",
    subtitle: "Turn insight into action",
    copy: "Convert each recommendation into a practical roadmap with curated resources and next steps."
  }
];

const roadmapMilestones = [
  {
    phase: "Phase 1",
    title: "Build foundations",
    copy: "Strengthen the core skills your target role expects before chasing advanced specialization."
  },
  {
    phase: "Phase 2",
    title: "Learn with resources",
    copy: "Use courses, videos, articles, documentation, and certifications to close your biggest gaps."
  },
  {
    phase: "Phase 3",
    title: "Create proof of work",
    copy: "Turn learning into projects, portfolio evidence, and confidence you can show in interviews."
  },
  {
    phase: "Phase 4",
    title: "Reassess and improve",
    copy: "Track progress over time, repeat assessments, and refine your path as your profile grows."
  }
];

export default function HomePage() {
  const location = useLocation();

  useEffect(() => {
    if (!location.hash) {
      return;
    }

    const target = document.querySelector(location.hash);
    if (target) {
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [location.hash]);

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
          </div>
        </div>
        <aside className="hero-panel">
          <h2>What this platform gives you</h2>
          <ul>
            <li>Live assessment powered by a real backend and database</li>
            <li>Top-match career scoring with clear fit explanations</li>
            <li>Skill-gap analysis and guided next-step resources</li>
            <li>Career detail pages with salaries, outlook, and core skill expectations</li>
            <li>Roadmap resources across courses, videos, articles, certifications, and docs</li>
            <li>Private assessment history so users can revisit and compare progress</li>
            <li>Admin tools for careers, skills, and roadmap content</li>
          </ul>
        </aside>
      </section>

      <section className="section" id="how-it-works">
        <p className="section-label">How it works</p>
        <div className="phase-grid">
          {phases.map((phase) => (
            <article className="phase-card" key={phase.step}>
              <div className="phase-step-row">
                <span className="phase-step-badge">{phase.step}</span>
                <span className="phase-step-line" aria-hidden="true" />
              </div>
              <div className="phase-copy">
                <span className="phase-kicker">{phase.subtitle}</span>
                <h3>{phase.title}</h3>
                <p>{phase.copy}</p>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="section" id="roadmap">
        <p className="section-label">Roadmap</p>
        <div className="roadmap-grid">
          {roadmapMilestones.map((item) => (
            <article className="roadmap-card" key={item.phase}>
              <span className="roadmap-pill">{item.phase}</span>
              <h3>{item.title}</h3>
              <p>{item.copy}</p>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
