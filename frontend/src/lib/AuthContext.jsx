import { createContext, useContext, useEffect, useMemo, useState } from "react";
import {
  clearAuthSession,
  fetchCurrentUser,
  getStoredUser,
  loginUser,
  persistAuthSession,
  registerUser
} from "./api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => getStoredUser());
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let ignore = false;

    async function hydrate() {
      if (!user) return;
      try {
        const currentUser = await fetchCurrentUser();
        if (!ignore) {
          setUser(currentUser);
        }
      } catch {
        clearAuthSession();
        if (!ignore) {
          setUser(null);
        }
      }
    }

    hydrate();
    return () => {
      ignore = true;
    };
  }, []);

  async function login(payload) {
    setLoading(true);
    try {
      const response = await loginUser(payload);
      persistAuthSession(response.access_token, response.user);
      setUser(response.user);
      return response.user;
    } finally {
      setLoading(false);
    }
  }

  async function register(payload) {
    setLoading(true);
    try {
      await registerUser(payload);
      return login({
        email: payload.email,
        password: payload.password
      });
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    clearAuthSession();
    setUser(null);
  }

  const value = useMemo(
    () => ({
      user,
      loading,
      isAuthenticated: Boolean(user),
      login,
      register,
      logout
    }),
    [user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider.");
  }
  return context;
}
