import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchSkills, submitAssessment } from "../lib/api";

const interestOptions = [
  { value: "tech", label: "Tech" },
  { value: "data", label: "Data" },
  { value: "business", label: "Business" },
  { value: "management", label: "Management" },
  { value: "design", label: "Design" }
];

const educationOptions = [
  { value: "ug", label: "Undergraduate" },
  { value: "pg", label: "Postgraduate" },
  { value: "diploma", label: "Diploma" }
];

const experienceOptions = [
  { value: "beginner", label: "Beginner" },
  { value: "intermediate", label: "Intermediate" },
  { value: "advanced", label: "Advanced" }
];

const workStyleOptions = [
  { value: "analytical", label: "Analytical" },
  { value: "creative", label: "Creative" },
  { value: "collaborative", label: "Collaborative" },
  { value: "structured", label: "Structured" }
];

const proficiencyOptions = [
  { value: "beginner", label: "Beginner" },
  { value: "intermediate", label: "Intermediate" },
  { value: "advanced", label: "Advanced" }
];

function normalizeError(error) {
  if (error instanceof Error) {
    return error.message;
  }
  return "Something went wrong. Please try again.";
}

export default function AssessmentPage() {
  const navigate = useNavigate();
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    interest_area: "data",
    education_level: "ug",
    experience_level: "beginner",
    preferred_domain: "analytics",
    work_style: "analytical",
    goal_salary: "900000",
    selectedSkills: {}
  });

  useEffect(() => {
    let ignore = false;

    async function loadSkills() {
      try {
        const data = await fetchSkills();
        if (!ignore) {
          setSkills(data);
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

    loadSkills();
    return () => {
      ignore = true;
    };
  }, []);

  function handleFieldChange(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  function toggleSkill(skillId) {
    setForm((current) => {
      const nextSelected = { ...current.selectedSkills };
      if (nextSelected[skillId]) {
        delete nextSelected[skillId];
      } else {
        nextSelected[skillId] = {
          proficiency_level: "beginner",
          years_of_experience: 0
        };
      }
      return { ...current, selectedSkills: nextSelected };
    });
  }

  function handleSkillMetaChange(skillId, field, value) {
    setForm((current) => ({
      ...current,
      selectedSkills: {
        ...current.selectedSkills,
        [skillId]: {
          ...current.selectedSkills[skillId],
          [field]:
            field === "years_of_experience" ? Number(value) || 0 : value
        }
      }
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    const selectedEntries = Object.entries(form.selectedSkills);
    if (!selectedEntries.length) {
      setError("Choose at least one skill so the recommendation engine has something to evaluate.");
      return;
    }

    const payload = {
      interest_area: form.interest_area,
      education_level: form.education_level,
      experience_level: form.experience_level,
      preferred_domain: form.preferred_domain || null,
      work_style: form.work_style || null,
      goal_salary: form.goal_salary ? Number(form.goal_salary) : null,
      skills: selectedEntries.map(([skillId, meta]) => ({
        skill_id: Number(skillId),
        proficiency_level: meta.proficiency_level,
        years_of_experience: Number(meta.years_of_experience) || 0
      }))
    };

    try {
      setSubmitting(true);
      const response = await submitAssessment(payload);
      navigate(`/results/${response.id}`);
    } catch (submitError) {
      setError(normalizeError(submitError));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="page">
      <section className="section-header">
        <p className="eyebrow">Live assessment</p>
        <h1 className="page-title">Build your career profile</h1>
        <p className="page-copy">
          Tell the system how you like to work, what you already know, and what kind
          of path you want to move toward.
        </p>
      </section>

      <form className="assessment-form" onSubmit={handleSubmit}>
        <div className="form-grid">
          <label className="field">
            <span>Interest area</span>
            <select name="interest_area" value={form.interest_area} onChange={handleFieldChange}>
              {interestOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>Education</span>
            <select name="education_level" value={form.education_level} onChange={handleFieldChange}>
              {educationOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>Experience level</span>
            <select name="experience_level" value={form.experience_level} onChange={handleFieldChange}>
              {experienceOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>Preferred domain</span>
            <input
              name="preferred_domain"
              value={form.preferred_domain}
              onChange={handleFieldChange}
              placeholder="analytics, product, ai"
            />
          </label>

          <label className="field">
            <span>Work style</span>
            <select name="work_style" value={form.work_style} onChange={handleFieldChange}>
              {workStyleOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>Goal salary</span>
            <input
              name="goal_salary"
              type="number"
              min="0"
              step="10000"
              value={form.goal_salary}
              onChange={handleFieldChange}
            />
          </label>
        </div>

        <section className="skills-section">
          <div className="skills-header">
            <div>
              <p className="section-label">Skill inventory</p>
              <h2>Choose the skills you already have</h2>
            </div>
            {loading ? <span className="status-chip">Loading skills...</span> : null}
          </div>

          <div className="skills-grid">
            {skills.map((skill) => {
              const selected = form.selectedSkills[skill.id];
              return (
                <article
                  className={`skill-card ${selected ? "skill-card-active" : ""}`}
                  key={skill.id}
                >
                  <label className="skill-toggle">
                    <input
                      type="checkbox"
                      checked={Boolean(selected)}
                      onChange={() => toggleSkill(skill.id)}
                    />
                    <div>
                      <strong>{skill.name}</strong>
                      <p>{skill.description}</p>
                    </div>
                  </label>

                  {selected ? (
                    <div className="skill-meta">
                      <label className="field">
                        <span>Proficiency</span>
                        <select
                          value={selected.proficiency_level}
                          onChange={(event) =>
                            handleSkillMetaChange(skill.id, "proficiency_level", event.target.value)
                          }
                        >
                          {proficiencyOptions.map((option) => (
                            <option key={option.value} value={option.value}>
                              {option.label}
                            </option>
                          ))}
                        </select>
                      </label>

                      <label className="field">
                        <span>Years</span>
                        <input
                          type="number"
                          min="0"
                          max="50"
                          value={selected.years_of_experience}
                          onChange={(event) =>
                            handleSkillMetaChange(
                              skill.id,
                              "years_of_experience",
                              event.target.value
                            )
                          }
                        />
                      </label>
                    </div>
                  ) : null}
                </article>
              );
            })}
          </div>
        </section>

        {error ? <p className="error-banner">{error}</p> : null}

        <div className="form-actions">
          <button type="submit" disabled={submitting || loading}>
            {submitting ? "Generating..." : "Get Recommendations"}
          </button>
        </div>
      </form>
    </div>
  );
}
