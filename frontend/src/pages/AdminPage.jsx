import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../lib/AuthContext";
import {
  createAdminCareer,
  createAdminResource,
  createAdminSkill,
  deleteAdminCareer,
  deleteAdminResource,
  deleteAdminSkill,
  fetchAdminAnalytics,
  fetchAdminCareers,
  fetchAdminResources,
  fetchAdminSkills,
  updateAdminCareer,
  updateAdminResource,
  updateAdminSkill
} from "../lib/api";

function normalizeError(error) {
  if (error instanceof Error) {
    return error.message;
  }
  return "Something went wrong.";
}

export default function AdminPage() {
  const { user, isAuthenticated } = useAuth();
  const [skills, setSkills] = useState([]);
  const [careers, setCareers] = useState([]);
  const [resources, setResources] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editingSkillId, setEditingSkillId] = useState(null);
  const [editingCareerId, setEditingCareerId] = useState(null);
  const [editingResourceId, setEditingResourceId] = useState(null);

  const [skillForm, setSkillForm] = useState({
    name: "",
    category: "technical",
    description: ""
  });

  const [careerForm, setCareerForm] = useState({
    title: "",
    slug: "",
    description: "",
    industry: "",
    growth_outlook: "",
    salary_min: "",
    salary_max: "",
    required_skills: []
  });

  const [resourceForm, setResourceForm] = useState({
    title: "",
    resource_type: "course",
    url: "",
    provider: "",
    difficulty_level: "",
    career_id: "",
    skill_id: ""
  });

  const isAdmin = user?.role === "admin";

  async function loadAdminData() {
    setLoading(true);
    setError("");
    try {
      const [analyticsData, skillData, careerData, resourceData] = await Promise.all([
        fetchAdminAnalytics(),
        fetchAdminSkills(),
        fetchAdminCareers(),
        fetchAdminResources()
      ]);
      setAnalytics(analyticsData);
      setSkills(skillData);
      setCareers(careerData);
      setResources(resourceData);
    } catch (loadError) {
      setError(normalizeError(loadError));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (!isAuthenticated || !isAdmin) {
      setLoading(false);
      return;
    }
    loadAdminData();
  }, [isAuthenticated, isAdmin]);

  function toggleCareerSkill(skillId) {
    setCareerForm((current) => {
      const exists = current.required_skills.some((item) => item.skill_id === skillId);
      return {
        ...current,
        required_skills: exists
          ? current.required_skills.filter((item) => item.skill_id !== skillId)
          : [
              ...current.required_skills,
              {
                skill_id: skillId,
                importance_level: "medium",
                is_required: true,
                weight: 1
              }
            ]
      };
    });
  }

  function updateCareerSkill(skillId, field, value) {
    setCareerForm((current) => ({
      ...current,
      required_skills: current.required_skills.map((item) =>
        item.skill_id === skillId
          ? {
              ...item,
              [field]: field === "weight" ? Number(value) || 1 : value
            }
          : item
      )
    }));
  }

  async function handleSkillSubmit(event) {
    event.preventDefault();
    try {
      if (editingSkillId) {
        await updateAdminSkill(editingSkillId, skillForm);
      } else {
        await createAdminSkill(skillForm);
      }
      setEditingSkillId(null);
      setSkillForm({ name: "", category: "technical", description: "" });
      await loadAdminData();
    } catch (submitError) {
      setError(normalizeError(submitError));
    }
  }

  async function handleCareerSubmit(event) {
    event.preventDefault();
    try {
      const payload = {
        ...careerForm,
        industry: careerForm.industry || null,
        growth_outlook: careerForm.growth_outlook || null,
        salary_min: careerForm.salary_min ? Number(careerForm.salary_min) : null,
        salary_max: careerForm.salary_max ? Number(careerForm.salary_max) : null
      };
      if (editingCareerId) {
        await updateAdminCareer(editingCareerId, payload);
      } else {
        await createAdminCareer(payload);
      }
      setEditingCareerId(null);
      setCareerForm({
        title: "",
        slug: "",
        description: "",
        industry: "",
        growth_outlook: "",
        salary_min: "",
        salary_max: "",
        required_skills: []
      });
      await loadAdminData();
    } catch (submitError) {
      setError(normalizeError(submitError));
    }
  }

  async function handleResourceSubmit(event) {
    event.preventDefault();
    try {
      const payload = {
        ...resourceForm,
        provider: resourceForm.provider || null,
        difficulty_level: resourceForm.difficulty_level || null,
        career_id: resourceForm.career_id ? Number(resourceForm.career_id) : null,
        skill_id: resourceForm.skill_id ? Number(resourceForm.skill_id) : null
      };
      if (editingResourceId) {
        await updateAdminResource(editingResourceId, payload);
      } else {
        await createAdminResource(payload);
      }
      setEditingResourceId(null);
      setResourceForm({
        title: "",
        resource_type: "course",
        url: "",
        provider: "",
        difficulty_level: "",
        career_id: "",
        skill_id: ""
      });
      await loadAdminData();
    } catch (submitError) {
      setError(normalizeError(submitError));
    }
  }

  async function handleDeleteSkill(skillId) {
    try {
      await deleteAdminSkill(skillId);
      if (editingSkillId === skillId) {
        setEditingSkillId(null);
        setSkillForm({ name: "", category: "technical", description: "" });
      }
      await loadAdminData();
    } catch (submitError) {
      setError(normalizeError(submitError));
    }
  }

  async function handleDeleteCareer(careerId) {
    try {
      await deleteAdminCareer(careerId);
      if (editingCareerId === careerId) {
        setEditingCareerId(null);
      }
      await loadAdminData();
    } catch (submitError) {
      setError(normalizeError(submitError));
    }
  }

  async function handleDeleteResource(resourceId) {
    try {
      await deleteAdminResource(resourceId);
      if (editingResourceId === resourceId) {
        setEditingResourceId(null);
        setResourceForm({
          title: "",
          resource_type: "course",
          url: "",
          provider: "",
          difficulty_level: "",
          career_id: "",
          skill_id: ""
        });
      }
      await loadAdminData();
    } catch (submitError) {
      setError(normalizeError(submitError));
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="page">
        <section className="empty-state">
          <h2>Login to access the admin area.</h2>
          <div className="history-actions">
            <Link className="primary-link" to="/login">
              Login
            </Link>
          </div>
        </section>
      </div>
    );
  }

  if (!isAdmin) {
    return (
      <div className="page">
        <section className="empty-state">
          <h2>Admin access required.</h2>
          <p className="page-copy">
            Your account is signed in but does not have admin privileges yet.
          </p>
        </section>
      </div>
    );
  }

  return (
    <div className="page">
      <section className="section-header">
        <p className="eyebrow">Admin</p>
        <h1 className="page-title">Content management</h1>
        <p className="page-copy">
          Manage skills, careers, and roadmap resources without editing code.
        </p>
      </section>

      {analytics ? (
        <section className="metric-row">
          <article className="metric-card">
            <span>Users</span>
            <strong>{analytics.total_users}</strong>
          </article>
          <article className="metric-card">
            <span>Assessments</span>
            <strong>{analytics.total_assessments}</strong>
          </article>
          <article className="metric-card">
            <span>Careers</span>
            <strong>{analytics.total_careers}</strong>
          </article>
          <article className="metric-card">
            <span>Skills</span>
            <strong>{analytics.total_skills}</strong>
          </article>
          <article className="metric-card">
            <span>Resources</span>
            <strong>{analytics.total_resources}</strong>
          </article>
        </section>
      ) : null}

      {error ? <p className="error-banner">{error}</p> : null}
      {loading ? <section className="empty-state"><h2>Loading admin data...</h2></section> : null}

      {!loading ? (
        <>
          {analytics ? (
            <section className="assessment-form">
              <p className="section-label">Recent assessments</p>
              <div className="result-grid">
                {analytics.recent_assessments.map((item) => (
                  <article className="result-card" key={item.assessment_id}>
                    <div className="result-card-top">
                      <div>
                        <h2>Assessment #{item.assessment_id}</h2>
                        <p>{item.interest_area}</p>
                      </div>
                      <span className="score-pill">
                        {new Date(item.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <div className="result-meta">
                      <span>{item.top_career || "No recommendation yet"}</span>
                      <span>{item.fit_score ? `${item.fit_score}% fit` : "Pending"}</span>
                    </div>
                  </article>
                ))}
              </div>
            </section>
          ) : null}

          <section className="admin-grid">
            <form className="assessment-form" onSubmit={handleSkillSubmit}>
              <p className="section-label">Create skill</p>
              <label className="field">
                <span>Name</span>
                <input
                  value={skillForm.name}
                  onChange={(event) =>
                    setSkillForm((current) => ({ ...current, name: event.target.value }))
                  }
                  required
                />
              </label>
              <label className="field">
                <span>Category</span>
                <select
                  value={skillForm.category}
                  onChange={(event) =>
                    setSkillForm((current) => ({ ...current, category: event.target.value }))
                  }
                >
                  <option value="technical">Technical</option>
                  <option value="domain">Domain</option>
                  <option value="tool">Tool</option>
                  <option value="soft">Soft</option>
                </select>
              </label>
              <label className="field">
                <span>Description</span>
                <input
                  value={skillForm.description}
                  onChange={(event) =>
                    setSkillForm((current) => ({ ...current, description: event.target.value }))
                  }
                />
              </label>
              <button type="submit">{editingSkillId ? "Update skill" : "Add skill"}</button>
            </form>

            <form className="assessment-form" onSubmit={handleResourceSubmit}>
              <p className="section-label">Create resource</p>
              <label className="field">
                <span>Title</span>
                <input
                  value={resourceForm.title}
                  onChange={(event) =>
                    setResourceForm((current) => ({ ...current, title: event.target.value }))
                  }
                  required
                />
              </label>
              <label className="field">
                <span>Type</span>
                <select
                  value={resourceForm.resource_type}
                  onChange={(event) =>
                    setResourceForm((current) => ({
                      ...current,
                      resource_type: event.target.value
                    }))
                  }
                >
                  <option value="course">Course</option>
                  <option value="project">Project</option>
                  <option value="article">Article</option>
                  <option value="video">Video</option>
                  <option value="certification">Certification</option>
                </select>
              </label>
              <label className="field">
                <span>URL</span>
                <input
                  value={resourceForm.url}
                  onChange={(event) =>
                    setResourceForm((current) => ({ ...current, url: event.target.value }))
                  }
                  required
                />
              </label>
              <label className="field">
                <span>Career</span>
                <select
                  value={resourceForm.career_id}
                  onChange={(event) =>
                    setResourceForm((current) => ({ ...current, career_id: event.target.value }))
                  }
                >
                  <option value="">None</option>
                  {careers.map((career) => (
                    <option key={career.id} value={career.id}>
                      {career.title}
                    </option>
                  ))}
                </select>
              </label>
              <button type="submit">{editingResourceId ? "Update resource" : "Add resource"}</button>
            </form>
          </section>

          <section className="assessment-form">
            <p className="section-label">Create career</p>
            <form className="admin-grid" onSubmit={handleCareerSubmit}>
              <label className="field">
                <span>Title</span>
                <input
                  value={careerForm.title}
                  onChange={(event) =>
                    setCareerForm((current) => ({ ...current, title: event.target.value }))
                  }
                  required
                />
              </label>
              <label className="field">
                <span>Slug</span>
                <input
                  value={careerForm.slug}
                  onChange={(event) =>
                    setCareerForm((current) => ({ ...current, slug: event.target.value }))
                  }
                  required
                />
              </label>
              <label className="field admin-span-2">
                <span>Description</span>
                <input
                  value={careerForm.description}
                  onChange={(event) =>
                    setCareerForm((current) => ({
                      ...current,
                      description: event.target.value
                    }))
                  }
                  required
                />
              </label>
              <label className="field">
                <span>Industry</span>
                <input
                  value={careerForm.industry}
                  onChange={(event) =>
                    setCareerForm((current) => ({ ...current, industry: event.target.value }))
                  }
                />
              </label>
              <label className="field">
                <span>Growth outlook</span>
                <input
                  value={careerForm.growth_outlook}
                  onChange={(event) =>
                    setCareerForm((current) => ({
                      ...current,
                      growth_outlook: event.target.value
                    }))
                  }
                />
              </label>
              <label className="field">
                <span>Salary min</span>
                <input
                  type="number"
                  value={careerForm.salary_min}
                  onChange={(event) =>
                    setCareerForm((current) => ({ ...current, salary_min: event.target.value }))
                  }
                />
              </label>
              <label className="field">
                <span>Salary max</span>
                <input
                  type="number"
                  value={careerForm.salary_max}
                  onChange={(event) =>
                    setCareerForm((current) => ({ ...current, salary_max: event.target.value }))
                  }
                />
              </label>

              <div className="admin-span-2">
                <p className="section-label">Required skills</p>
                <div className="skills-grid">
                  {skills.map((skill) => {
                    const selected = careerForm.required_skills.find(
                      (item) => item.skill_id === skill.id
                    );
                    return (
                      <article
                        className={`skill-card ${selected ? "skill-card-active" : ""}`}
                        key={skill.id}
                      >
                        <label className="skill-toggle">
                          <input
                            type="checkbox"
                            checked={Boolean(selected)}
                            onChange={() => toggleCareerSkill(skill.id)}
                          />
                          <div>
                            <strong>{skill.name}</strong>
                            <p>{skill.description}</p>
                          </div>
                        </label>
                        {selected ? (
                          <div className="skill-meta">
                            <label className="field">
                              <span>Importance</span>
                              <select
                                value={selected.importance_level}
                                onChange={(event) =>
                                  updateCareerSkill(
                                    skill.id,
                                    "importance_level",
                                    event.target.value
                                  )
                                }
                              >
                                <option value="low">Low</option>
                                <option value="medium">Medium</option>
                                <option value="high">High</option>
                              </select>
                            </label>
                            <label className="field">
                              <span>Weight</span>
                              <input
                                type="number"
                                min="1"
                                max="10"
                                value={selected.weight}
                                onChange={(event) =>
                                  updateCareerSkill(skill.id, "weight", event.target.value)
                                }
                              />
                            </label>
                          </div>
                        ) : null}
                      </article>
                    );
                  })}
                </div>
              </div>

              <div className="form-actions admin-span-2">
                <button type="submit">{editingCareerId ? "Update career" : "Add career"}</button>
              </div>
            </form>
          </section>

          <section className="result-grid">
            {careers.map((career) => (
              <article className="result-card" key={career.id}>
                <div className="result-card-top">
                  <div>
                    <h2>{career.title}</h2>
                    <p>{career.description}</p>
                  </div>
                  <span className="score-pill">{career.slug}</span>
                </div>
                <div className="result-meta">
                  <span>{career.industry || "No industry"}</span>
                  <span>{career.growth_outlook || "No outlook"}</span>
                </div>
                <div className="history-actions">
                  <button
                    type="button"
                    onClick={() => {
                      setEditingCareerId(career.id);
                      setCareerForm({
                        title: career.title,
                        slug: career.slug,
                        description: career.description,
                        industry: career.industry || "",
                        growth_outlook: career.growth_outlook || "",
                        salary_min: career.salary_min || "",
                        salary_max: career.salary_max || "",
                        required_skills: (career.required_skills || []).map((item) => ({
                          skill_id: item.skill_id,
                          importance_level: item.importance_level,
                          is_required: item.is_required,
                          weight: item.weight
                        }))
                      });
                    }}
                  >
                    Edit
                  </button>
                  <button type="button" onClick={() => handleDeleteCareer(career.id)}>
                    Delete
                  </button>
                </div>
              </article>
            ))}
          </section>

          <section className="admin-grid">
            <article className="result-card">
              <p className="section-label">Skills</p>
              {skills.map((skill) => (
                <div className="gap-item" key={skill.id}>
                  <strong>{skill.name}</strong>
                  <p>{skill.category}</p>
                  <div className="history-actions">
                    <button
                      type="button"
                      onClick={() => {
                        setEditingSkillId(skill.id);
                        setSkillForm({
                          name: skill.name,
                          category: skill.category,
                          description: skill.description || ""
                        });
                      }}
                    >
                      Edit
                    </button>
                    <button type="button" onClick={() => handleDeleteSkill(skill.id)}>
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </article>

            <article className="result-card">
              <p className="section-label">Resources</p>
              {resources.map((resource) => (
                <div className="gap-item" key={resource.id}>
                  <strong>{resource.title}</strong>
                  <p>{resource.resource_type}</p>
                  <div className="history-actions">
                    <button
                      type="button"
                      onClick={() => {
                        setEditingResourceId(resource.id);
                        setResourceForm({
                          title: resource.title,
                          resource_type: resource.resource_type,
                          url: resource.url,
                          provider: resource.provider || "",
                          difficulty_level: resource.difficulty_level || "",
                          career_id: resource.career_id || "",
                          skill_id: resource.skill_id || ""
                        });
                      }}
                    >
                      Edit
                    </button>
                    <button type="button" onClick={() => handleDeleteResource(resource.id)}>
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </article>
          </section>
        </>
      ) : null}
    </div>
  );
}
