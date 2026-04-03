import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchRecommendations, fetchResources } from "../lib/api";

function normalizeError(error) {
  if (error instanceof Error) {
    return error.message;
  }
  return "Unable to load recommendations.";
}

export default function ResultsPage() {
  const { assessmentId } = useParams();
  const [data, setData] = useState(null);
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let ignore = false;

    async function loadRecommendations() {
      try {
        const response = await fetchRecommendations(assessmentId);
        if (!ignore) {
          setData(response);
          if (response.recommendations?.[0]?.career_id) {
            const resourceResponse = await fetchResources({
              careerId: response.recommendations[0].career_id,
              limit: 3
            });
            if (!ignore) {
              setResources(resourceResponse);
            }
          }
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

    loadRecommendations();
    return () => {
      ignore = true;
    };
  }, [assessmentId]);

  if (loading) {
    return (
      <div className="page">
        <section className="empty-state">
          <p className="eyebrow">Loading</p>
          <h1 className="page-title">Generating your career matches...</h1>
        </section>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page">
        <section className="empty-state">
          <p className="eyebrow">Error</p>
          <h1 className="page-title">We could not load your results.</h1>
          <p className="page-copy">{error}</p>
          <Link className="primary-link" to="/assessment">
            Try assessment again
          </Link>
        </section>
      </div>
    );
  }

  const [topMatch, ...otherMatches] = data.recommendations;
  const gapLabelMap = {
    missing: "Missing now",
    recommended: "Worth adding",
    matched: "Already strong"
  };

  return (
    <div className="page">
      <section className="hero results-hero">
        <div>
          <p className="eyebrow">Assessment #{data.assessment_id}</p>
          <h1 className="page-title">Your top recommendation is {topMatch.career.title}.</h1>
          <p className="hero-copy">{topMatch.reason_summary}</p>
          <div className="metric-row">
            <div className="metric-card">
              <span>Fit score</span>
              <strong>{topMatch.fit_score}%</strong>
            </div>
            <div className="metric-card">
              <span>Confidence</span>
              <strong>{topMatch.confidence_score}%</strong>
            </div>
            <div className="metric-card">
              <span>Salary range</span>
              <strong>
                INR {topMatch.career.salary_min?.toLocaleString()} -{" "}
                {topMatch.career.salary_max?.toLocaleString()}
              </strong>
            </div>
          </div>
        </div>

        <aside className="hero-panel">
          <h2>Key gaps to close</h2>
          <ul>
            {topMatch.skill_gaps.map((gap) => (
              <li key={`${gap.skill_id}-${gap.gap_type}`}>{gap.note}</li>
            ))}
          </ul>
        </aside>
      </section>

      {resources.length ? (
        <section className="section">
          <p className="section-label">Recommended roadmap</p>
          <div className="resource-grid">
            {resources.map((resource) => (
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
                      {resource.provider || "Learning resource"} ·{" "}
                      {resource.difficulty_level || "all levels"}
                    </p>
                  </div>
                  <span className="score-pill">{resource.resource_type}</span>
                </div>
              </a>
            ))}
          </div>
        </section>
      ) : null}

      <section className="section">
        <p className="section-label">All recommendations</p>
        <div className="result-grid">
          {data.recommendations.map((item) => (
            <article className="result-card" key={item.id}>
              <div className="result-card-top">
                <div>
                  <h2>{item.rank}. {item.career.title}</h2>
                  <p>{item.career.description}</p>
                </div>
                <span className="score-pill">{item.fit_score}% fit</span>
              </div>

              <div className="result-meta">
                <span>{item.career.industry}</span>
                <span>{item.career.growth_outlook} growth</span>
                <span>Confidence {item.confidence_score}%</span>
              </div>

              <div className="gap-list">
                {item.skill_gaps.map((gap) => (
                  <div className="gap-item" key={`${item.id}-${gap.skill_id}-${gap.gap_type}`}>
                    <strong>{gapLabelMap[gap.gap_type] || gap.gap_type}</strong>
                    <p>{gap.note}</p>
                  </div>
                ))}
              </div>
            </article>
          ))}
        </div>
      </section>

      {otherMatches.length ? (
        <section className="section">
          <p className="section-label">Next move</p>
          <div className="roadmap-card">
            <p>
              The current engine now ranks paths and surfaces starter resources. Next we
              can add saved history, user accounts, and progress tracking.
            </p>
          </div>
        </section>
      ) : null}
    </div>
  );
}
