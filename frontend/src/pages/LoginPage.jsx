import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../lib/AuthContext";

export default function LoginPage() {
  const navigate = useNavigate();
  const { login, loading } = useAuth();
  const [form, setForm] = useState({ email: "", password: "" });
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
      await login(form);
      navigate("/history");
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Unable to log in.");
    }
  }

  return (
    <div className="page">
      <section className="auth-card">
        <p className="eyebrow">Login</p>
        <h1 className="page-title">Welcome back</h1>
        <p className="page-copy">Sign in to keep your assessment history tied to your account.</p>

        <form className="auth-form" onSubmit={handleSubmit}>
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
          {error ? <p className="error-banner">{error}</p> : null}
          <button type="submit" disabled={loading}>
            {loading ? "Signing in..." : "Login"}
          </button>
        </form>

        <p className="page-copy">
          New here? <Link to="/register">Create an account</Link>
        </p>
      </section>
    </div>
  );
}
