import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../lib/AuthContext";

export default function RegisterPage() {
  const navigate = useNavigate();
  const { register, loading } = useAuth();
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    password: "",
    education_level: "ug",
    experience_level: "beginner"
  });
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    try {
      await register(form);
      navigate("/history");
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Unable to create account.");
    }
  }

  return (
    <div className="page">
      <section className="auth-card">
        <p className="eyebrow">Register</p>
        <h1 className="page-title">Create your profile</h1>
        <p className="page-copy">Save your assessments and build a personal career roadmap.</p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label className="field">
            <span>Full name</span>
            <input
              name="full_name"
              value={form.full_name}
              onChange={handleChange}
              required
            />
          </label>
          <label className="field">
            <span>Email</span>
            <input name="email" type="email" value={form.email} onChange={handleChange} required />
          </label>
          <label className="field password-field">
            <span>Password</span>
            <div className="password-input-wrap">
              <input
                name="password"
                type={showPassword ? "text" : "password"}
                value={form.password}
                onChange={handleChange}
                required
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword((current) => !current)}
                aria-label={showPassword ? "Hide password" : "Show password"}
                aria-pressed={showPassword}
              >
                {showPassword ? "🙈" : "👁"}
              </button>
            </div>
          </label>
          <label className="field">
            <span>Education</span>
            <select
              name="education_level"
              value={form.education_level}
              onChange={handleChange}
            >
              <option value="ug">Undergraduate</option>
              <option value="pg">Postgraduate</option>
              <option value="diploma">Diploma</option>
            </select>
          </label>
          <label className="field">
            <span>Experience</span>
            <select
              name="experience_level"
              value={form.experience_level}
              onChange={handleChange}
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </label>
          {error ? <p className="error-banner">{error}</p> : null}
          <button type="submit" disabled={loading}>
            {loading ? "Creating..." : "Create account"}
          </button>
        </form>

        <p className="page-copy">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </section>
    </div>
  );
}
