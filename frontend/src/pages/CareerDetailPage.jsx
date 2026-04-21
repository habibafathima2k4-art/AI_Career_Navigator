import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  clearResourceProgress,
  fetchCareer,
  fetchResourceProgress,
  updateResourceProgress as persistResourceProgress
} from "../lib/api";
import { useAuth } from "../lib/AuthContext";

const resourceTypeMeta = {
  all: { label: "All" },
  course: { label: "Course" },
  project: { label: "Project" },
  article: { label: "Article" },
  video: { label: "Video" },
  certification: { label: "Certification" },
  documentation: { label: "Documentation" }
};

const progressLabelMap = {
  not_started: "Saved",
  in_progress: "In progress",
  completed: "Completed"
};

const projectSuggestionLibrary = {
  "ai engineer": [
    {
      title: "Inference API with model monitoring",
      summary: "Build and deploy a model-serving API with request logging, confidence output, and simple monitoring dashboards."
    },
    {
      title: "LLM workflow assistant",
      summary: "Create a prompt-driven assistant with retrieval, evaluation notes, and structured output formatting."
    }
  ],
  "data scientist": [
    {
      title: "End-to-end predictive model case study",
      summary: "Prepare a full notebook-to-report pipeline including cleaning, feature engineering, model comparison, and recommendations."
    },
    {
      title: "Experiment analysis dashboard",
      summary: "Analyze A/B or historical business data and present findings through charts, metrics, and actionable insights."
    }
  ],
  "data analyst": [
    {
      title: "Interactive KPI dashboard",
      summary: "Design a dashboard that tracks core business metrics with filters, drill-downs, and stakeholder-friendly summaries."
    },
    {
      title: "SQL reporting portfolio case",
      summary: "Use SQL plus visualization tools to clean data, answer business questions, and present insights clearly."
    }
  ],
  "bi analyst": [
    {
      title: "Executive reporting suite",
      summary: "Create a BI dashboard package with trend views, regional filters, and presentation-ready KPI commentary."
    },
    {
      title: "Data warehouse metrics model",
      summary: "Model business metrics from raw tables and document how each dashboard KPI is defined and refreshed."
    }
  ],
  "backend developer": [
    {
      title: "Production-ready REST API",
      summary: "Build a secure backend with authentication, CRUD routes, validation, and database integration."
    },
    {
      title: "Service integration project",
      summary: "Connect third-party APIs, background tasks, and persistence layers in a maintainable backend architecture."
    }
  ],
  "frontend developer": [
    {
      title: "Responsive product interface",
      summary: "Create a polished multi-page frontend with reusable components, routing, state handling, and accessibility basics."
    },
    {
      title: "Data-rich dashboard UI",
      summary: "Design an interactive dashboard with charts, filters, and clear information hierarchy."
    }
  ],
  "product manager": [
    {
      title: "Product strategy case study",
      summary: "Document a problem statement, user research insights, prioritization framework, roadmap, and success metrics."
    },
    {
      title: "Feature launch simulation",
      summary: "Prepare PRD-style documentation, stakeholder trade-offs, and go-to-market notes for a new product feature."
    }
  ],
  "business analyst": [
    {
      title: "Requirements and process mapping pack",
      summary: "Create business requirements, workflow diagrams, stakeholder notes, and measurable outcome definitions."
    },
    {
      title: "Operations improvement case",
      summary: "Analyze an existing workflow, identify bottlenecks, and propose documented process improvements."
    }
  ]
};

function buildResumeSuggestions(career, requiredSkills, supportSkills, resources) {
  const topRequired = requiredSkills.slice(0, 3).map((item) => item.skill.name);
  const topSupport = supportSkills.slice(0, 2).map((item) => item.skill.name);
  const resourceTypes = [...new Set(resources.map((resource) => resource.resource_type))];
  const normalizedTitle = career.title.toLowerCase();

  return [
    `Write a resume summary that positions you for ${career.title} roles and highlights ${topRequired.join(", ")} as your strongest capabilities.`,
    `Create an evidence-based skills section with tools, technologies, and methods you can actually demonstrate through coursework or projects.`,
    topSupport.length
      ? `Use support strengths like ${topSupport.join(" and ")} to show collaboration, communication, or business context alongside technical ability.`
      : `Show proof of execution through projects, measurable outcomes, and role-relevant responsibilities rather than listing skills only.`,
    resourceTypes.includes("certification")
      ? `Add a certifications subsection only if you complete relevant credentials and can connect them to practical work.`
      : `Prioritize portfolio evidence and measurable impact over certificates unless the target role specifically expects them.`,
    normalizedTitle.includes("manager") || normalizedTitle.includes("analyst")
      ? "Include bullet points that show problem framing, decision support, stakeholder communication, and real business impact."
      : "Use action-oriented bullet points that show implementation depth, problem solving, and the technologies you used end to end."
  ];
}

function buildProjectSuggestions(career, requiredSkills, resources) {
  const normalizedTitle = career.title.toLowerCase();
  const mappedProjects = projectSuggestionLibrary[normalizedTitle] || [
    {
      title: `${career.title} portfolio case study`,
      summary: "Build one complete project that demonstrates the core workflow, tools, and decisions expected in this role."
    },
    {
      title: `${career.title} practical showcase`,
      summary: "Prepare a second smaller project that shows role-specific depth, clear outcomes, and communication of results."
    }
  ];

  const topSkills = requiredSkills.slice(0, 3).map((item) => item.skill.name);
  const resourceTypes = [...new Set(resources.map((resource) => resource.resource_type))];

  return mappedProjects.map((project, index) => ({
    ...project,
    evidence:
      index === 0
        ? `Focus on proving ${topSkills.join(", ")} through one polished end-to-end build.`
        : `Support it with portfolio evidence such as ${resourceTypes.join(", ") || "projects and documentation"} that strengthen credibility.`
  }));
}

function normalizeError(error) {
  if (error instanceof Error) {
    return error.message;
  }
  return "Unable to load career details.";
}

export default function CareerDetailPage() {
  const { careerId } = useParams();
  const { user } = useAuth();
  const [career, setCareer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedResourceType, setSelectedResourceType] = useState("all");
  const [resourceProgress, setResourceProgress] = useState({});

  useEffect(() => {
    let ignore = false;

    async function loadCareer() {
      try {
        const response = await fetchCareer(careerId);
        let progressResponse = [];

        if (user) {
          try {
            progressResponse = await fetchResourceProgress({ careerId });
          } catch {
            progressResponse = [];
          }
        }

        if (!ignore) {
          setCareer(response);
          setResourceProgress(
            Object.fromEntries(progressResponse.map((entry) => [entry.resource_id, entry.status]))
          );
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
  }, [careerId, user]);

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
  const resumeSuggestions = buildResumeSuggestions(career, requiredSkills, supportSkills, careerResources);
  const projectSuggestions = buildProjectSuggestions(career, requiredSkills, careerResources);
  const progressSummary = careerResources.reduce(
    (summary, resource) => {
      const status = resourceProgress[resource.id];
      if (status && summary[status] !== undefined) {
        summary[status] += 1;
      }
      return summary;
    },
    { not_started: 0, in_progress: 0, completed: 0 }
  );

  async function updateResourceProgress(resourceId, status) {
    if (!user) {
      setError("Login to save roadmap progress across devices.");
      return;
    }

    const previous = resourceProgress[resourceId];
    const nextStatus = previous === status ? null : status;

    setResourceProgress((current) => {
      const next = { ...current };
      if (nextStatus) {
        next[resourceId] = nextStatus;
      } else {
        delete next[resourceId];
      }
      return next;
    });

    try {
      if (nextStatus) {
        await persistResourceProgress(resourceId, nextStatus);
      } else {
        await clearResourceProgress(resourceId);
      }
    } catch (progressError) {
      setResourceProgress((current) => {
        const reverted = { ...current };
        if (previous) {
          reverted[resourceId] = previous;
        } else {
          delete reverted[resourceId];
        }
        return reverted;
      });
      setError(normalizeError(progressError));
    }
  }

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

      <section className="section career-detail-grid">
        <article className="roadmap-card suggestion-card">
          <p className="section-label">Resume suggestions</p>
          <p className="page-copy suggestion-copy">
            Use these points to shape a stronger resume, LinkedIn summary, and interview story for this role.
          </p>
          <div className="suggestion-list">
            {resumeSuggestions.map((point) => (
              <div className="suggestion-item" key={point}>
                <span className="suggestion-bullet">+</span>
                <p>{point}</p>
              </div>
            ))}
          </div>
        </article>

        <article className="roadmap-card suggestion-card">
          <p className="section-label">Project ideas</p>
          <p className="page-copy suggestion-copy">
            Build 1 to 2 portfolio pieces like these to make your profile more convincing for {career.title} opportunities.
          </p>
          <div className="suggestion-list">
            {projectSuggestions.map((project) => (
              <div className="suggestion-item suggestion-item-project" key={project.title}>
                <div>
                  <strong>{project.title}</strong>
                  <p>{project.summary}</p>
                  <small>{project.evidence}</small>
                </div>
              </div>
            ))}
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
            {!user ? (
              <p className="page-copy resource-section-copy">
                Login to save progress across devices.
              </p>
            ) : null}
          </div>
          <div className="resource-controls">
            <div className="resource-filter-row">
              {availableResourceTypes.map((type) => {
                const meta = resourceTypeMeta[type] || { label: type };
                const count =
                  type === "all"
                    ? careerResources.length
                    : careerResources.filter((resource) => resource.resource_type === type).length;
                return (
                  <button
                    className={`filter-chip ${selectedResourceType === type ? "filter-chip-active" : ""}`}
                    key={type}
                    onClick={() => setSelectedResourceType(type)}
                    type="button"
                  >
                    {meta.label} ({count})
                  </button>
                );
              })}
            </div>
            <div className="progress-summary-row">
              {Object.entries(progressLabelMap).map(([status, label]) => (
                <span className={`progress-summary-chip progress-chip-${status}`} key={status}>
                  {label}: {progressSummary[status]}
                </span>
              ))}
            </div>
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
                <div className="resource-progress-row">
                  {Object.entries(progressLabelMap).map(([status, label]) => (
                    <button
                      className={`progress-chip ${resourceProgress[resource.id] === status ? "progress-chip-active" : ""} progress-chip-${status}`}
                      key={status}
                      onClick={(event) => {
                        event.preventDefault();
                        event.stopPropagation();
                        updateResourceProgress(resource.id, status);
                      }}
                      type="button"
                    >
                      {label}
                    </button>
                  ))}
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
