import { Link, Outlet } from "react-router-dom";
import { useAuth } from "../lib/AuthContext";

export default function AppShell() {
  const { isAuthenticated, logout, user } = useAuth();

  return (
    <div className="app-shell">
      <header className="site-header">
        <Link className="brand" to="/">
          AI Career Navigator
        </Link>
        <nav className="site-nav">
          <Link to="/admin">Admin</Link>
          <Link to="/assessment">Assessment</Link>
          <Link to="/history">History</Link>
          <a href="#how-it-works">How it works</a>
          <a href="#roadmap">Roadmap</a>
        </nav>
        <div className="auth-nav">
          {isAuthenticated ? (
            <>
              <span className="api-badge">{user?.full_name}</span>
              <button type="button" onClick={logout}>
                Logout
              </button>
            </>
          ) : (
            <>
              <Link className="ghost-link" to="/login">
                Login
              </Link>
              <Link className="primary-link" to="/register">
                Register
              </Link>
            </>
          )}
        </div>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  );
}
