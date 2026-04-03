import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../lib/AuthContext";
import { fetchAssessments } from "../lib/api";

function normalizeError(error) {
  if (error instanceof Error) {
    return error.message;
  }
  return "Unable to load assessment history.";
}

export default function HistoryPage() {
  const { isAuthenticated } = useAuth();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let ignore = false;

    if (!isAuthenticated) {
      setItems([]);
      setLoading(false);
      setError("");
      return () => {
        ignore = true;
      };
    }

    async function loadHistory() {
      try {
        const response = await fetchAssessments();
        if (!ignore) {
          setItems(response);
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

    loadHistory();
    return () => {
      ignore = true;
    };
  }, [isAuthenticated]);

  return (
    <div className="page">
      <section className="section-header">
        <p className="eyebrow">History</p>
        <h1 className="page-title">Past assessments</h1>
        <p className="page-copy">
          Reopen any recommendation set and compare how your profile evolves over time.
        </p>
      </section>

      {!isAuthenticated ? (
        <section className="empty-state">
          <h2>Login to view your saved assessments.</h2>
          <p className="page-copy">
            History is now private to each account.
          </p>
          <div className="history-actions">
            <Link className="primary-link" to="/login">
              Login
            </Link>
          </div>
        </section>
      ) : null}

      {loading ? (
        <section className="empty-state">
          <h2>Loading assessments...</h2>
        </section>
      ) : null}

      {error ? <p className="error-banner">{error}</p> : null}

      {!loading && !error && isAuthenticated ? (
        <section className="result-grid">
          {items.map((item) => (
            <article className="result-card" key={item.id}>
              <div className="result-card-top">
                <div>
                  <h2>Assessment #{item.id}</h2>
                  <p>
                    {item.interest_area} · {item.education_level} · {item.experience_level}
                  </p>
                </div>
                <span className="score-pill">
                  {new Date(item.created_at).toLocaleDateString()}
                </span>
              </div>

              <div className="result-meta">
                <span>Domain: {item.preferred_domain || "not specified"}</span>
                <span>Work style: {item.work_style || "not specified"}</span>
              </div>

              {item.top_recommendation ? (
                <div className="gap-item">
                  <strong>Top match</strong>
                  <p>
                    {item.top_recommendation.career_title} · {item.top_recommendation.fit_score}% fit
                  </p>
                  <p>{item.top_recommendation.reason_summary}</p>
                </div>
              ) : (
                <div className="gap-item">
                  <strong>No recommendations yet</strong>
                  <p>This assessment does not have generated matches yet.</p>
                </div>
              )}

              <div className="history-actions">
                <Link className="primary-link" to={`/results/${item.id}`}>
                  View results
                </Link>
              </div>
            </article>
          ))}
        </section>
      ) : null}
    </div>
  );
}
