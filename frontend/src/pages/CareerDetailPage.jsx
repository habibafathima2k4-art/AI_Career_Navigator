import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchCareer } from "../lib/api";

const resourceTypeMeta = {
  all: { label: "All" },
  course: { label: "Course" },
  project: { label: "Project" },
  article: { label: "Article" },
  video: { label: "Video" },
  certification: { label: "Certification" },
  documentation: { label: "Documentation" }
};

function normalizeError(error) {
  if (error instanceof Error) {
    return error.message;
  }
  return "Unable to load career details.";
}

export default function CareerDetailPage() {
  const { careerId } = useParams();
  const [career, setCareer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedResourceType, setSelectedResourceType] = useState("all");

  useEffect(() => {
    let ignore = false;

    async function loadCareer() {
      try {
        const response = await fetchCareer(careerId);
        if (!ignore) {
          setCareer(response);
        }
      } catch (loadError) {
        if (!ignore) {
          setError(normalizeError(loadError));
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    loadCareer();
    return () => {
      ignore = true;
    };
  }, [careerId]);

  useEffect(() => {
    setSelectedResourceType("all");
  }, [careerId]);

  if (loading) {
    return (
      <div className="page">
        <section className="empty-state">
          <p className="eyebrow">Loading</p>
          <h1 className="page-title">Opening career profile...</h1>
        </section>
      </div>
    );
  }

  if (error || !career) {
    return (
      <div className="page">
        <section className="empty-state">
          <p className="eyebrow">Error</p>
          <h1 className="page-title">We could not load this career.</h1>
          <p className="page-copy">{error || "Career not found."}</p>
          <Link className="primary-link" to="/assessment">
            Back to assessment
          </Link>
        </section>
      </div>
    );
  }

  const careerResources = career.learning_resources || [];
  const careerSkills = career.required_skills || [];
  const requiredSkills = careerSkills.filter((item) => item.is_required);
  const supportSkills = careerSkills.filter((item) => !item.is_required);
  const availableResourceTypes = [
    "all",
    ...new Set(careerResources.map((resource) => resource.resource_type).filter(Boolean))
  ];
  const visibleResources =
    selectedResourceType === "all"
      ? careerResources
      : careerResources.filter((resource) => resource.resource_type === selectedResourceType);

  return (
    <div className="page">
      <section className="hero results-hero">
        <div>
          <p className="eyebrow">Career profile</p>
          <h1 className="page-title">{career.title}</h1>
          <p className="hero-copy">{career.description}</p>

          <div className="metric-row">
            <div className="metric-card">
              <span>Industry</span>
              <strong>{career.industry || "General"}</strong>
            </div>
            <div className="metric-card">
              <span>Growth outlook</span>
              <strong>{career.growth_outlook || "Stable"}</strong>
            </div>
            <div className="metric-card">
              <span>Salary range</span>
              <strong>
                INR {career.salary_min?.toLocaleString()} - {career.salary_max?.toLocaleString()}
              </strong>
            </div>
          </div>
        </div>

        <aside className="hero-panel">
          <h2>How to approach this path</h2>
          <ul>
            <li>Build strength in the required skills first.</li>
            <li>Use the roadmap resources to close missing gaps steadily.</li>
            <li>Track your progress through repeat assessments over time.</li>
          </ul>
        </aside>
      </section>

      <section className="section career-detail-grid">
        <article className="roadmap-card">
          <p className="section-label">Core skills</p>
          <div className="gap-list">
            {requiredSkills.map((item) => (
              <div className="gap-item" key={item.skill_id}>
                <strong>{item.skill.name}</strong>
                <p>{item.skill.description}</p>
              </div>
            ))}
          </div>
        </article>

        <article className="roadmap-card">
          <p className="section-label">Support skills</p>
          <div className="gap-list">
            {supportSkills.length ? (
              supportSkills.map((item) => (
                <div className="gap-item" key={item.skill_id}>
                  <strong>{item.skill.name}</strong>
                  <p>{item.skill.description}</p>
                </div>
              ))
            ) : (
              <div className="gap-item">
                <strong>Focused skill set</strong>
                <p>This path is currently modeled with a compact core-skill profile.</p>
              </div>
            )}
          </div>
        </article>
      </section>

      <section className="section">
        <div className="resource-section-header">
          <div>
            <p className="section-label">Roadmap resources</p>
            <p className="page-copy resource-section-copy">
              Filter this roadmap by resource type to focus on the learning format you want.
            </p>
          </div>
          <div className="resource-filter-row">
            {availableResourceTypes.map((type) => {
              const meta = resourceTypeMeta[type] || { label: type };
              return (
                <button
                  className={`filter-chip ${selectedResourceType === type ? "filter-chip-active" : ""}`}
                  key={type}
                  onClick={() => setSelectedResourceType(type)}
                  type="button"
                >
                  {meta.label}
                </button>
              );
            })}
          </div>
        </div>
        <div className="resource-grid">
          {visibleResources.length ? (
            visibleResources.map((resource) => (
              <a
                className="resource-card"
                href={resource.url}
                key={resource.id}
                rel="noreferrer"
                target="_blank"
              >
                <div className="result-card-top">
                  <div>
                    <h2>{resource.title}</h2>
                    <p>
                      {resource.provider || "Learning resource"} |{" "}
                      {resource.difficulty_level || "all levels"}
                    </p>
                  </div>
                  <span className={`score-pill resource-type-badge resource-badge-${resource.resource_type}`}>
                    {resourceTypeMeta[resource.resource_type]?.label || resource.resource_type}
                  </span>
                </div>
              </a>
            ))
          ) : (
            <div className="empty-state">
              <h2>No matching resources</h2>
              <p className="page-copy">
                Try a different filter to view more roadmap resources for this career.
              </p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
