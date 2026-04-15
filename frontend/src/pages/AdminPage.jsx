import { useEffect, useRef, useState } from "react";
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

const resourceTypeMeta = {
  course: { icon: "◎", label: "Course", className: "resource-badge-course" },
  project: { icon: "◧", label: "Project", className: "resource-badge-project" },
  article: { icon: "◫", label: "Article", className: "resource-badge-article" },
  video: { icon: "▶", label: "Video", className: "resource-badge-video" },
  certification: { icon: "★", label: "Certification", className: "resource-badge-certification" },
  documentation: { icon: "≣", label: "Documentation", className: "resource-badge-documentation" }
};

function normalizeError(error) {
  if (error instanceof Error) {
    return error.message;
  }
  return "Something went wrong.";
}

export default function AdminPage() {
  const { user, isAuthenticated } = useAuth();
  const skillFormRef = useRef(null);
  const resourceFormRef = useRef(null);
  const careerFormRef = useRef(null);
  const [skills, setSkills] = useState([]);
  const [careers, setCareers] = useState([]);
  const [resources, setResources] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [editingSkillId, setEditingSkillId] = useState(null);
  const [editingCareerId, setEditingCareerId] = useState(null);
  const [editingResourceId, setEditingResourceId] = useState(null);
  const [skillSearch, setSkillSearch] = useState("");
  const [resourceSearch, setResourceSearch] = useState("");

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
  const normalizedSkillSearch = skillSearch.trim().toLowerCase();
  const normalizedResourceSearch = resourceSearch.trim().toLowerCase();
  const visibleSkills = skills.filter((skill) => {
    if (!normalizedSkillSearch) return true;
    return `${skill.name} ${skill.description || ""} ${skill.category || ""}`
      .toLowerCase()
      .includes(normalizedSkillSearch);
  });
  const visibleResources = resources.filter((resource) => {
    if (!normalizedResourceSearch) return true;
    return `${resource.title} ${resource.provider || ""} ${resource.resource_type || ""}`
      .toLowerCase()
      .includes(normalizedResourceSearch);
  });

  function jumpToForm(formRef) {
    window.requestAnimationFrame(() => {
      formRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
      const firstInput = formRef.current?.querySelector("input, select, textarea");
      if (firstInput instanceof HTMLElement) {
        firstInput.focus();
      }
    });
  }

  function resetSkillForm() {
    setEditingSkillId(null);
    setSkillForm({ name: "", category: "technical", description: "" });
  }

  function resetCareerForm() {
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
  }

  function resetResourceForm() {
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
    setError("");
    setSuccess("");
    try {
      if (editingSkillId) {
        await updateAdminSkill(editingSkillId, skillForm);
        setSuccess("Skill updated successfully.");
      } else {
        await createAdminSkill(skillForm);
        setSuccess("Skill added successfully.");
      }
      resetSkillForm();
      await loadAdminData();
    } catch (submitError) {
      setError(normalizeError(submitError));
    }
  }

  async function handleCareerSubmit(event) {
    event.preventDefault();
    setError("");
    setSuccess("");
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
        setSuccess("Career updated successfully.");
      } else {
        await createAdminCareer(payload);
        setSuccess("Career added successfully.");
      }
      resetCareerForm();
      await loadAdminData();
    } catch (submitError) {
      setError(normalizeError(submitError));
    }
  }

  async function handleResourceSubmit(event) {
    event.preventDefault();
    setError("");
    setSuccess("");
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
        setSuccess("Resource updated successfully.");
      } else {
        await createAdminResource(payload);
        setSuccess("Resource added successfully.");
      }
      resetResourceForm();
      await loadAdminData();
    } catch (submitError) {
      setError(normalizeError(submitError));
    }
  }

  async function handleDeleteSkill(skillId) {
    if (!window.confirm("Delete this skill?")) {
      return;
    }
    setError("");
    setSuccess("");
    try {
      await deleteAdminSkill(skillId);
      if (editingSkillId === skillId) {
        resetSkillForm();
      }
      setSuccess("Skill deleted successfully.");
      await loadAdminData();
    } catch (submitError) {
      setError(normalizeError(submitError));
    }
  }

  async function handleDeleteCareer(careerId) {
    if (!window.confirm("Delete this career?")) {
      return;
    }
    setError("");
    setSuccess("");
    try {
      await deleteAdminCareer(careerId);
      if (editingCareerId === careerId) {
        resetCareerForm();
      }
      setSuccess("Career deleted successfully.");
      await loadAdminData();
    } catch (submitError) {
      setError(normalizeError(submitError));
    }
  }

  async function handleDeleteResource(resourceId) {
    if (!window.confirm("Delete this resource?")) {
      return;
    }
    setError("");
    setSuccess("");
    try {
      await deleteAdminResource(resourceId);
      if (editingResourceId === resourceId) {
        resetResourceForm();
      }
      setSuccess("Resource deleted successfully.");
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
      {success ? <p className="success-banner">{success}</p> : null}
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

          <section className="admin-grid admin-form-grid">
            <form
              className={`assessment-form admin-skill-form ${editingSkillId ? "admin-skill-form-editing" : ""}`}
              onSubmit={handleSkillSubmit}
              ref={skillFormRef}
            >
              <div className="admin-skill-form-header">
                <div>
                  <p className="section-label">{editingSkillId ? "Edit skill" : "Create skill"}</p>
                  <h2 className="admin-card-title">
                    {editingSkillId ? "Update the selected skill" : "Add a new skill to the catalog"}
                  </h2>
                </div>
                <span className="admin-skill-status">
                  {editingSkillId ? "Editing live item" : "New entry"}
                </span>
              </div>
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
              <p className="admin-form-note">
                Keep the skill name short, choose the closest category, and write a one-line
                description that explains how the skill is used in recommendations.
              </p>
              <div className="history-actions">
                <button type="submit">{editingSkillId ? "Update skill" : "Add skill"}</button>
                {editingSkillId ? (
                  <button className="secondary-button" type="button" onClick={resetSkillForm}>
                    Cancel
                  </button>
                ) : null}
              </div>
            </form>

            <form
              className={`assessment-form admin-skill-form ${editingResourceId ? "admin-skill-form-editing" : ""}`}
              onSubmit={handleResourceSubmit}
              ref={resourceFormRef}
            >
              <div className="admin-skill-form-header">
                <div>
                  <p className="section-label">{editingResourceId ? "Edit resource" : "Create resource"}</p>
                  <h2 className="admin-card-title">
                    {editingResourceId ? "Update the selected resource" : "Add a new roadmap resource"}
                  </h2>
                </div>
                <span className="admin-skill-status">
                  {editingResourceId ? "Editing live item" : "New entry"}
                </span>
              </div>
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
                  <option value="documentation">Documentation</option>
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
              <p className="admin-form-note">
                Add a clear title, choose the right type, and attach the resource to the most
                relevant career so it appears in the roadmap section properly.
              </p>
              <div className="history-actions">
                <button type="submit">
                  {editingResourceId ? "Update resource" : "Add resource"}
                </button>
                {editingResourceId ? (
                  <button
                    className="secondary-button"
                    type="button"
                    onClick={resetResourceForm}
                  >
                    Cancel
                  </button>
                ) : null}
              </div>
            </form>
          </section>

          <section className="assessment-form">
            <p className="section-label">{editingCareerId ? "Edit career" : "Create career"}</p>
            <form className="admin-grid" onSubmit={handleCareerSubmit} ref={careerFormRef}>
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
                <div className="skills-grid admin-required-skills-grid">
                  {skills.map((skill) => {
                    const selected = careerForm.required_skills.find(
                      (item) => item.skill_id === skill.id
                    );
                    return (
                      <article
                        className={`skill-card admin-required-skill-card ${selected ? "skill-card-active" : ""}`}
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
                <div className="history-actions">
                  <button type="submit">
                    {editingCareerId ? "Update career" : "Add career"}
                  </button>
                  {editingCareerId ? (
                    <button
                      className="secondary-button"
                      type="button"
                      onClick={resetCareerForm}
                    >
                      Cancel
                    </button>
                  ) : null}
                </div>
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
                    className="admin-action-button"
                    type="button"
                    onClick={() => {
                      setError("");
                      setSuccess("Editing career loaded into the form below.");
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
                      jumpToForm(careerFormRef);
                    }}
                  >
                    Edit
                  </button>
                  <button
                    className="admin-action-button admin-delete-button"
                    type="button"
                    onClick={() => handleDeleteCareer(career.id)}
                  >
                    Delete
                  </button>
                </div>
              </article>
            ))}
          </section>

          <section className="admin-grid">
            <article className="result-card admin-scroll-panel">
              <div className="admin-panel-header">
                <div>
                  <p className="section-label">Skills</p>
                  <p className="admin-panel-count">{visibleSkills.length} visible</p>
                </div>
                <label className="field admin-panel-search">
                  <span>Search</span>
                  <input
                    placeholder="Python, SQL, communication..."
                    value={skillSearch}
                    onChange={(event) => setSkillSearch(event.target.value)}
                  />
                </label>
              </div>
              <div className="admin-skill-list">
              {visibleSkills.map((skill) => (
                <div
                  className={`gap-item admin-skill-item ${editingSkillId === skill.id ? "admin-skill-item-active" : ""}`}
                  key={skill.id}
                >
                  <div className="admin-skill-row">
                    <div className="admin-skill-copy">
                      <strong>{skill.name}</strong>
                      <p>{skill.description || "No description added yet."}</p>
                    </div>
                    <span className="admin-category-badge">{skill.category}</span>
                  </div>
                  <div className="history-actions">
                    <button
                      className="admin-action-button"
                      type="button"
                      onClick={() => {
                        setError("");
                        setSuccess("Editing skill loaded into the form above.");
                        setEditingSkillId(skill.id);
                        setSkillForm({
                          name: skill.name,
                          category: skill.category,
                          description: skill.description || ""
                        });
                        jumpToForm(skillFormRef);
                      }}
                    >
                      Edit
                    </button>
                    <button
                      className="admin-action-button admin-delete-button"
                      type="button"
                      onClick={() => handleDeleteSkill(skill.id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
              </div>
            </article>

            <article className="result-card admin-scroll-panel">
              <div className="admin-panel-header">
                <div>
                  <p className="section-label">Resources</p>
                  <p className="admin-panel-count">{visibleResources.length} visible</p>
                </div>
                <label className="field admin-panel-search">
                  <span>Search</span>
                  <input
                    placeholder="course, docs, certification..."
                    value={resourceSearch}
                    onChange={(event) => setResourceSearch(event.target.value)}
                  />
                </label>
              </div>
              <div className="admin-skill-list">
              {visibleResources.map((resource) => {
                const meta = resourceTypeMeta[resource.resource_type] || {
                  icon: "•",
                  label: resource.resource_type,
                  className: ""
                };
                return (
                <div className="gap-item admin-skill-item" key={resource.id}>
                  <div className="admin-skill-row">
                    <div className="admin-skill-copy">
                      <strong>{resource.title}</strong>
                      <p>{resource.provider || resource.resource_type}</p>
                    </div>
                    <span className={`admin-category-badge resource-type-badge ${meta.className}`}>
                      <span aria-hidden="true">{meta.icon}</span> {meta.label}
                    </span>
                  </div>
                  <div className="history-actions">
                    <button
                      className="admin-action-button"
                      type="button"
                      onClick={() => {
                        setError("");
                        setSuccess("Editing resource loaded into the form above.");
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
                        jumpToForm(resourceFormRef);
                      }}
                    >
                      Edit
                    </button>
                    <button
                      className="admin-action-button admin-delete-button"
                      type="button"
                      onClick={() => handleDeleteResource(resource.id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
                );
              })}
              </div>
            </article>
          </section>
        </>
      ) : null}
    </div>
  );
}
